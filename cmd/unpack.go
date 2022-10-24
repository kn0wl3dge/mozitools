package cmd

import (
	"github.com/kn0wl3dge/mozitools/pkg/unpack"
	"github.com/spf13/cobra"
	"log"
	"path/filepath"
)

var unpackInputPath string
var unpackOutputPath string
var unpackCmd = &cobra.Command{
	Use:     "unpack",
	Aliases: []string{"unp", "un"},
	Short:   "Unpack a Mozi sample",
	Args:    cobra.ExactArgs(0),
	Run: func(cmd *cobra.Command, args []string) {
		log.Printf("Running Mozi unpacker on %s\n", unpackInputPath)
		err := unpack.Unpack(unpackInputPath, unpackOutputPath)
		if err != nil {
			log.Fatalf("An error occured during unpacking: %s\n", err)
		} else {
			absPath, _ := filepath.Abs(unpackOutputPath)
			log.Printf("Unpacked Mozi sample in %s\n", absPath)
		}
	},
}

func init() {
	unpackCmd.Flags().StringVarP(&unpackInputPath, "input", "i", "", "Path to packed Mozi sample")
	unpackCmd.Flags().StringVarP(&unpackOutputPath, "output", "o", "", "Path to store the unpacked Mozi sample")
	unpackCmd.MarkFlagRequired("input")
	unpackCmd.MarkFlagRequired("output")
	rootCmd.AddCommand(unpackCmd)
}
