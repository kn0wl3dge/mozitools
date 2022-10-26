package track

import (
	"bytes"
	"context"
	"crypto/tls"
	"encoding/hex"
	"encoding/json"
	"log"
	"net"
	"net/http"
	"strconv"
	"strings"
	"time"

	"github.com/elastic/go-elasticsearch/v8"
	"github.com/elastic/go-elasticsearch/v8/esutil"
	"github.com/kn0wl3dge/mozitools/pkg/decode/config"
)

type Mozi struct {
	cnf    *config.MoziConfig
	nodeId *string
	addr   *net.UDPAddr
}

type ELKMozi struct {
	Time   string        `json:"timestamp"`
	Config ELKMoziConfig `json:"config"`
	Node   ELKMoziNode   `json:"node"`
}

type ELKMoziConfig struct {
	Raw        string            `json:"raw"`
	Version    int               `json:"version"`
	Signature1 string            `json:"signature1"`
	Signature2 string            `json:"signature2"`
	Fields     map[string]string `json:"fields"`
}

type ELKMoziNode struct {
	NodeId string `json:"node_id"`
	IP     string `json:"ip"`
	Port   int    `json:"port"`
}

type ELKClient struct {
	es    *elasticsearch.Client
	bi    *esutil.BulkIndexer
	nodes chan *Mozi
}

type ELKConfig struct {
	Url   string
	Index string
	User  string
	Pass  string
}

func NewELKClient(elkConfig ELKConfig) *ELKClient {
	transport := http.DefaultTransport
	transport.(*http.Transport).TLSClientConfig = &tls.Config{InsecureSkipVerify: true}
	cfg := elasticsearch.Config{
		Addresses: []string{
			elkConfig.Url,
		},
		Username:  elkConfig.User,
		Password:  elkConfig.Pass,
		Transport: transport,
	}
	es, err := elasticsearch.NewClient(cfg)
	if err != nil {
		log.Printf("Could not create a new elasticsearch client: %s\n", err)
		return nil
	}
	_, err = es.Info()
	if err != nil {
		log.Printf("Error getting response: %s", err)
		return nil
	}

	bi, err := esutil.NewBulkIndexer(esutil.BulkIndexerConfig{
		Index:         elkConfig.Index,  // The default index name
		Client:        es,               // The Elasticsearch client
		NumWorkers:    3,                // The number of worker goroutines
		FlushBytes:    100000,           // The flush threshold in bytes
		FlushInterval: 10 * time.Second, // The periodic flush interval
	})
	if err != nil {
		log.Printf("Could not create a new elasticsearch bulk indexer: %s\n", err)
		return nil
	}
	c := make(chan *Mozi, 1000)
	return &ELKClient{
		es:    es,
		bi:    &bi,
		nodes: c,
	}
}

func createELKMoziDocument(input *Mozi) []byte {
	data := ELKMozi{
		Time: strconv.FormatInt(time.Now().Unix(), 10),
		Config: ELKMoziConfig{
			Raw:        strings.Trim(string(input.cnf.Rawdata[:]), "\x00"),
			Version:    input.cnf.Version,
			Signature1: hex.EncodeToString(input.cnf.Signature1[:]),
			Signature2: hex.EncodeToString(input.cnf.Signature2[:]),
			Fields:     input.cnf.Fields,
		},
		Node: ELKMoziNode{
			NodeId: hex.EncodeToString([]byte(*input.nodeId)),
			IP:     input.addr.IP.String(),
			Port:   input.addr.Port,
		},
	}
	output, err := json.Marshal(data)
	if err != nil {
		log.Printf("Could not marshal the ELKMozi struct: %s\n", err)
		output = nil
	}
	return output
}

func (e *ELKClient) processMoziNodes() {
	log.Println("Running the elasticsearch client...")
	for {
		node := <-e.nodes
		doc := createELKMoziDocument(node)
		if doc != nil {
			_ = (*(e.bi)).Add(
				context.Background(),
				esutil.BulkIndexerItem{
					Action: "index",
					Body:   bytes.NewReader(doc),
				},
			)
		}
	}
}
