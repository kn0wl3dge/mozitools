package track

import (
	"crypto/rand"
	lru "github.com/hashicorp/golang-lru"
	"github.com/kn0wl3dge/mozitools/pkg/decode"
	"github.com/kn0wl3dge/mozitools/pkg/decode/config"
	"log"
	"net"
	"os"
	"os/signal"
	"strconv"
	"syscall"
	"time"
)

const MOZI_NODE_ID_PREFIX = "88888888"
const DEFAULT_MOZI_NODE_ID = "88888888888888888888"

type MoziTracker struct {
	dht   *DHTClient
	elk   *ELKClient
	nodes chan *net.UDPAddr
	cache *lru.Cache
}

func randomMoziId() string {
	random := make([]byte, 12)
	length, err := rand.Read(random)
	if err != nil || length != 12 {
		return DEFAULT_MOZI_NODE_ID
	}
	return MOZI_NODE_ID_PREFIX + string(random)
}

func NewMoziTracker(elkConfig ELKConfig) *MoziTracker {
	c := make(chan *net.UDPAddr, 1000)
	dht := NewDHTClient(randomMoziId())
	elk := NewELKClient(elkConfig)
	cache, err := lru.New(100000)
	if dht == nil || elk == nil || err != nil {
		return nil
	}
	return &MoziTracker{
		dht:   dht,
		elk:   elk,
		nodes: c,
		cache: cache,
	}
}

func (m *MoziTracker) Run() {
	log.Println("Running Mozi tracker...")
	go m.scanDHTNetwork()
	go m.parseDHTResponses()
	go m.elk.processMoziNodes()

	done := make(chan os.Signal, 1)
	signal.Notify(done, syscall.SIGINT, syscall.SIGTERM)
	<-done
}

func (m *MoziTracker) scanDHTNetwork() {
	log.Println("Running the Mozi DHT scanner...")
	go func() {
		for {
			for i := range BOOTSTRAP_NODES {
				addr, err := net.ResolveUDPAddr("udp", BOOTSTRAP_NODES[i])
				if err != nil {
					continue
				}
				m.nodes <- addr
			}
			time.Sleep(100 * time.Millisecond)
		}
	}()

	for {
		addr := <-m.nodes
		m.dht.findNodes(addr, randomMoziId())
	}
}

func (m *MoziTracker) parseDHTResponses() {
	log.Println("Running the Mozi DHT responses parser...")
	for {
		addr, nodeId, nodes := m.dht.findNodesResponse()
		if addr == nil || nodeId == nil || nodes == nil {
			continue
		}
		if string((*nodes)[:4]) == decode.MOZI_CNF_ENC_HEADER {
			hash := addr.IP.String() + strconv.Itoa(addr.Port) + *nodeId
			exists, _ := m.cache.ContainsOrAdd(hash, 1)
			cnf, err := config.NewMoziConfig(*nodes, true)
			if err == nil && exists == false {
				n := &Mozi{
					cnf:    cnf,
					nodeId: nodeId,
					addr:   addr,
				}
				m.elk.nodes <- n
			}
		} else {
			for i := 0; i+26 <= len(*nodes); i += 26 {
				node := parseDHTNodeFromBuffer((*nodes)[i : i+26])
				if node != nil {
					m.nodes <- node.addr
				}
			}
		}
	}
}
