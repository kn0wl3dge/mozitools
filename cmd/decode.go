package cmd

import (
	"github.com/kn0wl3dge/mozitools/pkg/decode"
	"github.com/spf13/cobra"
	"log"
	"path/filepath"
)

var decodeInputPath string
var decodeCmd = &cobra.Command{
	Use:     "decode",
	Aliases: []string{"dec", "de"},
	Short:   "Decode a Mozi configuration",
	Args:    cobra.ExactArgs(0),
	Run: func(cmd *cobra.Command, args []string) {
		absPath, _ := filepath.Abs(decodeInputPath)
		log.Printf("Running Mozi decoder on %s\n", absPath)
		err := decode.DecodeMoziFile(decodeInputPath)
		if err != nil {
			log.Fatalf("An error occured during unpacking: %s\n", err)
		} else {
			log.Println("Successfully decoded Mozi configuration!")
		}
	},
}

func init() {
	decodeCmd.Flags().StringVarP(&decodeInputPath, "input", "i", "", "Path to unpacked Mozi sample")
	unpackCmd.MarkFlagRequired("input")
	rootCmd.AddCommand(decodeCmd)
}
