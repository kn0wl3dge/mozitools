package decode

import (
	"bytes"
	"fmt"
	"github.com/kn0wl3dge/mozitools/pkg/decode/config"
	"os"
)

const MOZI_CNF_ENC_HEADER = "\x15\x15\x29\xD2"

func DecodeMoziFile(path string) error {
	data, err := os.ReadFile(path)
	if err != nil {
		return err
	}

	index := bytes.Index(data, []byte(MOZI_CNF_ENC_HEADER)) // [ss] ^ KEY[:4]
	if index == -1 {
		return fmt.Errorf("Could not find the encrypted configuration of %s\n", path)
	}
	cnf, err := config.NewMoziConfig(data[index:index+config.MOZI_CNF_LEN], true)
	if err != nil {
		return err
	}

	cnf.Show()
	return nil
}
