# Mozitools

## Features
* Repair the UPX p_info structure (p_filesize and p_blocksize are set to null
  to avoid unpacking)
* Unpack the sample using UPX
* Recover and decrypt the configuration of the sample
* Track the botnet using the DHT protocol to simulate a Mozi node and query other node configurations
* Import Mozi configurations extracted by the tracker in ElasticSearch

## Requirements
* UPX must be installed and available in the user PATH

## Usage
```bash
$ ./mozitools -h

  __  __          _ _              _     
 |  \/  | ___ ___(_) |_ ___   ___ | |___ 
 | |\/| |/ _ \_  / | __/ _ \ / _ \| / __|
 | |  | | (_) / /| | || (_) | (_) | \__ \
 |_|  |_|\___/___|_|\__\___/ \___/|_|___/
                                         

mozitools facilites RE of Mozi malwares. 
It can:
        * Repair the UPX p_info structure (p_filesize and p_blocksize are set to null to avoid unpacking)
        * Unpack the sample using UPX
        * Recover and decrypt the configuration of the sample
        * Fake a Mozi node and request config files
        * Find others Mozi nodes and import results in ElasticSearch

Usage:
  mozitools [flags]
  mozitools [command]

Available Commands:
  completion  Generate the autocompletion script for the specified shell
  decode      Decode a Mozi configuration
  help        Help about any command
  track       Track Mozi compromised nodes
  unpack      Unpack a Mozi sample

Flags:
  -h, --help   help for mozitools

Use "mozitools [command] --help" for more information about a command.



$ ./mozitools unp -i Mozi.m -o Mozi
2022/10/24 22:28:33 Running Mozi unpacker on Mozi.m
2022/10/24 22:28:33 Found UPX at /usr/local/bin/upx
2022/10/24 22:28:33 Unpacked file SHA256: 8f3a5bc6088b999d50bce0eef02c41860bc8ac5e63a2379508c20a1c188eb38d
Unpacked Mozi sample in /Users/baptistin/Documents/Projects/dev/mozitools/Mozi


$ ./mozitools dec -i Mozi
2022/10/24 22:28:49 Running Mozi decoder on /Users/baptistin/Documents/Projects/dev/mozitools/Mozi
2022/10/24 22:28:49 Mozi raw configuration:
    5b73735d626f7476325b2f73735d5b6469705d3139322e3136382e322e3130303a38305b2f6469705d5b68705d38383838383838385b2f68705d5b636f756e745d687474703a2f2f69612e35312e6c612f676f313f69643d31373637353132352670753d68747470253361253266253266762e62616964752e636f6d2f5b6964705d5b2f636f756e745d0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

2022/10/24 22:28:49 Mozi configuration signature1:
    b0e74673720d660dd4a369e706576943f6be4f71966516acb1c842d5bf36cfc86717caf562b1fbc12b0a80fab170217ba2aa3e3bad1844af856320add9c1f8afe2eac3acf522c7737d7568551b902b926fd65c969a2c4f34aa4a380fe2ada249

2022/10/24 22:28:49 Mozi configuration signature2:
    c33f318d0bee9747640f78bbb90b9b4192c325d178e7e50575d67c3566917abee559b6cf1acb5d2bc4db08a420afea4d921a2e6dff86cc92e603ce6987f2f2a100e8408f2c184a53ccb29978bbd16261e964ee7e80aa86296d9880429a31e1cf

2022/10/24 22:28:49 Mozi configuration version: 2

2022/10/24 22:28:49 Parsed Mozi configuration:
2022/10/24 22:28:49     [ss   ] (Bot role                    ) -> botv2
2022/10/24 22:28:49     [hp   ] (DHT node hash prefix        ) -> 88888888
2022/10/24 22:28:49     [count] (URL that used to report bot ) -> http://ia.51.la/go1?id=17675125&pu=http%3a%2f%2fv.baidu.com/
2022/10/24 22:28:49     [idp  ] (report bot                  ) -> true
2022/10/24 22:28:49     [dip  ] (ip:port to download Mozi bot) -> 192.168.2.100:80
2022/10/24 22:28:49 
2022/10/24 22:28:49 Successfully decoded Mozi configuration!


$ ./mozitools track --index mozi-test --url https://127.0.0.1:9200 --user elastic --pass elastic
2022/10/24 22:45:14 Running Mozi tracker...
2022/10/24 22:45:14 Running the elasticsearch client...
2022/10/24 22:45:14 Running the Mozi DHT scanner...
2022/10/24 22:45:14 Running the Mozi DHT responses parser...
^C
```

## Try it

A container file is available to try out Mozitools !

To create the image : 
```
podman build -t mozitools -f Containerfile
```

To test Mozitools :

```
podman run -v $PWD:/app/data mozitools unp -i data/Mozi.m -o data/Mozi
```

# How does it work?
You can check out this [Blog Article](https://kn0wledge.fr/projects/mozitools) for more
information.

# Submit an issue

Feel free to submit any issue you could encounter. I'll be happy to provide a
fix.  
Please, do not forget to add details related to your issue (command line
, output, sample...).

# References
* https://www.cyberdefensemagazine.com/mozi-botnet-is-responsible-for-most-of-the-iot-traffic/
* https://securityintelligence.com/posts/botnet-attack-mozi-mozied-into-town/
* https://blog.netlab.360.com/mozi-another-botnet-using-dht/
* https://blag.nullteilerfrei.de/2019/12/26/upx-packed-elf-binaries-of-the-peer-to-peer-botnet-family-mozi/
* https://cujo.com/upx-anti-unpacking-techniques-in-iot-malware/
* https://blog.lumen.com/new-mozi-malware-family-quietly-amasses-iot-bots/
* https://threatpost.com/mozi-botnet-majority-iot-traffic/159337/


