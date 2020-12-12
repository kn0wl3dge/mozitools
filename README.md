# Mozitools

## Features
* Repair the UPX p_info structure (p_filesize and p_blocksize are set to null
 to avoid unpacking)
* Unpack the sample using UPX
* Recover and decrypt the configuration of the sample
* Fake a Mozi node and request config files
* Find others Mozi nodes and import results in ElasticSearch

## Usage
```bash
pip install -r requirements.txt
python ./mozitools.py -h
```

## Running requirements
* This code is tested and maintained using python 3
* UPX should be installed and available in the PATH

## Dev requirements
```bash
pip install -r requirements.txt
pip install -r dev-requirements.txt
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

