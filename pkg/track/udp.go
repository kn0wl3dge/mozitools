package track

import (
	"bytes"
	"github.com/jackpal/bencode-go"
	"log"
	"net"
)

type UDPMsg struct {
	data []byte
	addr net.Addr
}

type UDPClient struct {
	conn     *net.UDPConn
	messages chan UDPMsg
}

func NewUDPClient() *UDPClient {
	client := UDPClient{}
	conn, err := net.ListenUDP("udp", nil)
	if err != nil {
		log.Printf("Could not on a random UDP port: %s\n", err)
		return nil
	}
	client.conn = conn
	client.messages = make(chan UDPMsg, 10)
	return &client
}

func (u *UDPClient) sendMsg(raddr *net.UDPAddr, query interface{}) {
	var b bytes.Buffer
	err := bencode.Marshal(&b, query)
	if err != nil {
		log.Printf("Could not bencode the DHT query: %s\n", err)
		return
	}
	data := b.Bytes()
	writeLen, err := u.conn.WriteToUDP(data, raddr)
	if err != nil {
		log.Printf("Could not send UDP packet to %v raddr: %s\n", raddr, err)
	}
	if writeLen != len(data) {
		log.Println("Got a short write while trying to send UDP packet.")
	}
}

func (u *UDPClient) recvMsg(response *responseType) *net.UDPAddr {
	// Handle the case where unmarshal crashes which sometime happen...
	defer func() {
		recover()
	}()

	buf := make([]byte, 1024)
	_, addr, err := u.conn.ReadFromUDP(buf)
	if err != nil {
		log.Printf("Could not read from UDP socket: %s\n", err)
		return nil
	}
	err = bencode.Unmarshal(bytes.NewBuffer(buf), response)
	if err != nil {
		// This is too verbose and not really useful
		// log.Printf("Could not unmashal the bencoded response: %s\n", err)
		return nil
	}
	return addr
}
