#Introduction

##Features
* Repair the UPX p_info structure (p_filesize and p_blocksize are set to null
 to avoid unpacking)
* Unpack the sample using UPX
* Recover and decrypt the configuration of the sample

##Usage


##Runnning requirements
* UPX should be installed and available in the PATH

##Dev requirements
```bash
pip install -r dev-requirements.txt
```

#How does it work ?
##Unpacking the sample
toto
##Extracting configuration file

#TODO
- [x] Implement the unpacker component
- [x] Implement the decoder component
- [ ] Add a config signature check
- [ ] Downloads samples using URLHaus
- [ ] Extract config from every samples
- [ ] Track the C2 / compromised host etc...


#References
* https://www.cyberdefensemagazine.com/mozi-botnet-is-responsible-for-most-of-the-iot-traffic/
* https://securityintelligence.com/posts/botnet-attack-mozi-mozied-into-town/
* https://blog.netlab.360.com/mozi-another-botnet-using-dht/
* https://blag.nullteilerfrei.de/2019/12/26/upx-packed-elf-binaries-of-the-peer-to-peer-botnet-family-mozi/
* https://cujo.com/upx-anti-unpacking-techniques-in-iot-malware/
* https://blog.lumen.com/new-mozi-malware-family-quietly-amasses-iot-bots/
* https://threatpost.com/mozi-botnet-majority-iot-traffic/159337/

