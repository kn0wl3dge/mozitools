package cmd

import (
	"github.com/spf13/cobra"
)

var rootCmd = &cobra.Command{
	Use:   "mozitools",
	Short: "mozitools - a set of tools to manipulate Mozi malwares",
	Long: `
  __  __          _ _              _     
 |  \/  | ___ ___(_) |_ ___   ___ | |___ 
 | |\/| |/ _ \_  / | __/ _ \ / _ \| / __|
 | |  | | (_) / /| | || (_) | (_) | \__ \
 |_|  |_|\___/___|_|\__\___/ \___/|_|___/
                                         

mozitools facilites RE of Mozi malwares. 
It can:
	* Repair the UPX p_info structure (p_filesize and p_blocksize are set to null
  to avoid unpacking)
	* Unpack the sample using UPX
	* Recover and decrypt the configuration of the sample
	* Track the botnet using the DHT protocol to simulate a Mozi node and query other node configurations
	* Import Mozi configurations extracted by the tracker in ElasticSearch`,
	Run: func(cmd *cobra.Command, args []string) {
		cmd.Help()
	},
}

func Execute() error {
	return rootCmd.Execute()
}
