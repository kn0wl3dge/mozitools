package config

import (
	"bytes"
	"fmt"
	"log"
	"regexp"
	"strings"
)

type MoziConfigFields map[string]string

var MOZI_CNF_TAGS = map[string]string{
	"ss":    "Bot role",
	"ssx":   "enable/disable tag [ss]",
	"cpu":   "CPU architecture",
	"cpux":  "enable/disable tag [cpu]",
	"nd":    "new DHT node",
	"hp":    "DHT node hash prefix",
	"atk":   "DDoS attack type",
	"ver":   "Value in V section in DHT protcol",
	"sv":    "Update config",
	"ud":    "Update bot",
	"dr":    "Download and execute payload from the specified URL",
	"rn":    "Execute specified command",
	"dip":   "ip:port to download Mozi bot",
	"idp":   "report bot",
	"count": "URL that used to report bot",
}

func NewMoziConfigFields(data string) (*MoziConfigFields, error) {
	cnf := MoziConfigFields{}
	cnf["idp"] = "false"
	for key, _ := range MOZI_CNF_TAGS {
		re, err := regexp.Compile(fmt.Sprintf("\\[%s\\](.*)\\[/%s\\]", key, key))
		if err != nil {
			return nil, err
		}
		match := re.FindStringSubmatch(data)
		if len(match) > 0 {
			if key == "count" && bytes.Index([]byte(match[1]), []byte("[idp]")) != -1 {
				cnf["idp"] = "true"
				cnf["count"] = strings.Replace(match[1], "[idp]", "", -1)
			} else {
				cnf[key] = match[1]
			}
		}
	}
	return &cnf, nil
}

func (c *MoziConfigFields) Show() {
	log.Println("Parsed Mozi configuration:")
	maxDescLen := 0
	for key, _ := range *c {
		if len(MOZI_CNF_TAGS[key]) > maxDescLen {
			maxDescLen = len(MOZI_CNF_TAGS[key])
		}
	}

	for key, val := range *c {
		log.Printf("\t[%-5s] (%-*s) -> %s\n", key, maxDescLen, MOZI_CNF_TAGS[key], val)
	}
	log.Println("")
}
