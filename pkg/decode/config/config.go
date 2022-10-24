package config

import (
	"encoding/binary"
	"errors"
	"fmt"
	"log"
)

const (
	MOZI_CNF_DATA_LEN      = 428
	MOZI_CNF_VERSION_LEN   = 4
	MOZI_CNF_SIGNATURE_LEN = 96
	MOZI_CNF_LEN           = MOZI_CNF_DATA_LEN + MOZI_CNF_VERSION_LEN + 2*MOZI_CNF_SIGNATURE_LEN
	MOZI_CNF_XOR_ENC_KEY   = "\x4E\x66\x5A\x8F\x80\xC8\xAC\x23\x8D\xAC\x47\x06\xD5\x4F\x6F\x7E"
)

type MoziConfig struct {
	Rawdata    [MOZI_CNF_DATA_LEN]byte
	Version    int
	Signature1 [MOZI_CNF_SIGNATURE_LEN]byte
	Signature2 [MOZI_CNF_SIGNATURE_LEN]byte
	Fields     MoziConfigFields
}

func NewMoziConfig(data []byte, encrypted bool) (*MoziConfig, error) {
	if len(data) != MOZI_CNF_LEN {
		return nil, fmt.Errorf("could not create a MoziConfig: rawdata length (%d) != %d", len(data), MOZI_CNF_LEN)
	}

	if encrypted {
		for i := 0; i < MOZI_CNF_DATA_LEN; i++ {
			data[i] ^= MOZI_CNF_XOR_ENC_KEY[i%len(MOZI_CNF_XOR_ENC_KEY)]
		}
	}

	index := 0
	cnf := new(MoziConfig)
	copy(cnf.Rawdata[:], data[index:MOZI_CNF_DATA_LEN])
	index += MOZI_CNF_DATA_LEN
	copy(cnf.Signature1[:], data[index:index+MOZI_CNF_SIGNATURE_LEN])
	index += MOZI_CNF_SIGNATURE_LEN
	cnf.Version = int(binary.LittleEndian.Uint32(data[index : index+MOZI_CNF_VERSION_LEN]))
	index += MOZI_CNF_VERSION_LEN
	copy(cnf.Signature2[:], data[index:index+MOZI_CNF_SIGNATURE_LEN])

	parsedCnf, err := NewMoziConfigFields(string(cnf.Rawdata[:]))
	if err != nil {
		return nil, errors.New("could not create MoziConfigFields")
	}

	cnf.Fields = *parsedCnf
	return cnf, nil
}

func (c *MoziConfig) Show() {
	log.Printf("Mozi raw configuration:\n\t%x\n\n", c.Rawdata)
	log.Printf("Mozi configuration signature1:\n\t%x\n\n", c.Signature1)
	log.Printf("Mozi configuration signature2:\n\t%x\n\n", c.Signature2)
	log.Printf("Mozi configuration version: %d\n\n", c.Version)
	c.Fields.Show()
}
