package track

import (
	"encoding/binary"
	"fmt"
	"log"
	"net"
)

var BOOTSTRAP_NODES = []string{
	"router.bittorrent.com:6881",
	"dht.transmissionbt.com:6881",
	"router.utorrent.com:6881",
	"bttracker.debian.org:6881",
	"212.129.33.59:6881",
	"82.221.103.244:6881",
	"130.239.18.159:6881",
	"87.98.162.88:6881",
}

type DHTClient struct {
	udp    *UDPClient
	nodeId string
}

type DHTNode struct {
	nodeId string
	ip     string
	port   int
	addr   *net.UDPAddr
}

type queryMessage struct {
	T string                 "t"
	Y string                 "y"
	Q string                 "q"
	A map[string]interface{} "a"
	V string                 "v"
}

type getPeersResponse struct {
	Values []string "values"
	Id     string   "id"
	Nodes  string   "nodes"
	Nodes6 string   "nodes6"
	Token  string   "token"
}

type responseType struct {
	T string                 "t"
	Y string                 "y"
	Q string                 "q"
	R getPeersResponse       "r"
	E []string               "e"
	A map[string]interface{} "a"
	V string                 "v"
}

func NewDHTClient(nodeId string) *DHTClient {
	udp := NewUDPClient()
	if udp == nil {
		return nil
	}
	return &DHTClient{
		udp:    udp,
		nodeId: nodeId,
	}
}

func (d *DHTClient) findNodes(addr *net.UDPAddr, nodeId string) {
	msg := queryMessage{
		"1",
		"q",
		"find_node",
		map[string]interface{}{
			"id":     d.nodeId,
			"target": nodeId,
		},
		"\x44\x42\x1f\x71",
	}
	d.udp.sendMsg(addr, msg)
}

func (d *DHTClient) findNodesResponse() (*net.UDPAddr, *string, *[]byte) {
	resp := responseType{}
	addr := d.udp.recvMsg(&resp)
	if addr == nil {
		return nil, nil, nil
	}
	nodes := []byte(resp.R.Nodes)
	if len(nodes) == 0 {
		return nil, nil, nil
	}
	return addr, &resp.R.Id, &nodes
}

func parseDHTNodeFromBuffer(data []byte) *DHTNode {
	if len(data) != 26 {
		log.Printf("The DHTNode length is invalid: %d != 26\n", len(data))
		return nil
	}
	node := DHTNode{
		nodeId: string(data[:20]),
		ip:     net.IP(data[20:24]).String(),
		port:   int(binary.BigEndian.Uint16(data[24:26])),
	}
	addr, err := net.ResolveUDPAddr("udp", fmt.Sprintf("%s:%d", node.ip, node.port))
	if err != nil {
		log.Printf("Could not resolve UDP address: %s\n", err)
		return nil
	}
	node.addr = addr
	return &node
}
