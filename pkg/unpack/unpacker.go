package unpack

import (
	"bytes"
	"crypto/sha256"
	"errors"
	"io"
	"log"
	"os"
	"os/exec"
)

func Unpack(inputPath string, outputPath string) error {
	if !isUPXInstalled() {
		return errors.New("UPX not installed")
	}

	data, err := os.ReadFile(inputPath)
	if err != nil {
		return err
	}

	err = fixUPXHeader(data)
	if err != nil {
		return err
	}

	err = os.WriteFile(outputPath, data, 0644)
	if err != nil {
		return err
	}

	upxCmd := exec.Command("upx", "-d", outputPath)
	out, err := upxCmd.Output()
	if err != nil {
		os.Remove(outputPath)
		return err
	}
	if bytes.Index(out, []byte("Unpacked 1 file.")) == -1 {
		os.Remove(outputPath)
		return errors.New("not packed by UPX (maybe not a Mozi sample)")
	}

	err = printFileSHA256(outputPath)
	if err != nil {
		return err
	}
	return nil
}

func fixUPXHeader(data []byte) error {
	if len(data) < 12 {
		return errors.New("packed data length to short")
	}
	pFilesize := data[len(data)-12 : len(data)-8]

	lInfoIndex := bytes.Index(data, []byte("UPX!")) - 4
	if lInfoIndex == -1 {
		return errors.New("could not find UPX l_info struct")
	}

	for i := 0; i < 8; i++ {
		data[lInfoIndex+16+i] = pFilesize[i%len(pFilesize)]
	}
	return nil
}

func isUPXInstalled() bool {
	path, err := exec.LookPath("upx")
	if err != nil {
		log.Println("Please install UPX. It is needed by the unpacking component.")
		return false
	}
	log.Printf("Found UPX at %s\n", path)
	return true
}

func printFileSHA256(path string) error {
	file, err := os.Open(path)
	if err != nil {
		return err
	}
	defer file.Close()

	hash := sha256.New()
	_, err = io.Copy(hash, file)
	if err != nil {
		return err
	}

	log.Printf("Unpacked file SHA256: %x\n", hash.Sum(nil))
	return nil
}
