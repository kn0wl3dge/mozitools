package cmd

import (
	"github.com/kn0wl3dge/mozitools/pkg/track"
	"github.com/spf13/cobra"
	"log"
)

var (
	trackUrl   string
	trackIndex string
	trackUser  string
	trackPass  string
)

var trackCmd = &cobra.Command{
	Use:     "track",
	Aliases: []string{"tra", "tr"},
	Short:   "Track Mozi compromised nodes",
	Run: func(cmd *cobra.Command, args []string) {
		elk := track.ELKConfig{
			Url:   trackUrl,
			Index: trackIndex,
			User:  trackUser,
			Pass:  trackPass,
		}
		t := track.NewMoziTracker(elk)
		if t == nil {
			log.Fatalln("An error occurred when loading the tracker")
		} else {
			t.Run()
		}
	},
}

func init() {
	trackCmd.Flags().StringVarP(&trackUrl, "url", "", "", "Elasticsearch URL")
	trackCmd.MarkFlagRequired("url")
	trackCmd.Flags().StringVarP(&trackIndex, "index", "", "", "Elasticsearch Index")
	trackCmd.MarkFlagRequired("index")
	trackCmd.Flags().StringVarP(&trackUser, "user", "", "", "Elasticsearch Pass")
	trackCmd.MarkFlagRequired("user")
	trackCmd.Flags().StringVarP(&trackPass, "pass", "", "", "Elasticsearch User")
	trackCmd.MarkFlagRequired("pass")
	rootCmd.AddCommand(trackCmd)
}
