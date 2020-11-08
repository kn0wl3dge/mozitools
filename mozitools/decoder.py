import json
import re

from mozitools.conf import *


class MoziConfigNotFoundError(Exception):
    """Raised when the decoder can't find the config of the sample."""


class MoziConfigParsingError(Exception):
    """Raised when the decoder is not able to parse the config of the sample."""


class MoziDecoder:
    """
    This class is used to decode Mozi v2 sample
    Example:
        d = MoziDecoder(unpacked_filename)
        decoded_config = d.decode()
    """
    def __init__(self, filename):
        self.filename = filename
        self.config = {}
        self.data = None

    def read_file(self):
        with open(self.filename, 'rb') as fd:
            self.data = fd.read()

    def decrypt_config(self, data):
        data = list(data)
        for i in range(len(data)):
            data[i] ^= XOR_KEY[i % len(XOR_KEY)]
        return ''.join(map(chr, data))

    def extract_config(self):
        config_index = self.data.index(CONFIG_HEADER)
        if config_index == -1:
            raise MoziConfigNotFoundError
        print(f"[+] Found config at offset: ({hex(config_index)})")
        raw_cfg = self.data[config_index:config_index + CONFIG_TOTAL_SIZE]

        begin = 0
        end = CONFIG_SIZE
        try:
            self.config["raw_config"] = self.decrypt_config(raw_cfg[begin:end])
            begin = end
            end += SIGNATURE1_SIZE
            self.config["signature1"] = raw_cfg[begin:end].hex()
            begin = end
            end += CONFIG_VERSION_SIZE
            self.config["version"] = int.from_bytes(raw_cfg[begin:end],'little')
            begin = end
            end += SIGNATURE2_SIZE
            self.config["signature2"] = raw_cfg[begin:end].hex()
            self.config["config"] = {}
            assert end == CONFIG_TOTAL_SIZE
        except IndexError:
            raise MoziConfigParsingError


    def parse_config(self):
        print("[+] Parsing the configuration...")

        for tag, desc in CONFIG_TAGS.items():
            regex = re.compile(rf'\[{tag}\](.*)\[/{tag}\]')
            res = regex.findall(self.config["raw_config"])
            if len(res) != 0:
                self.config["config"][tag] = {"desc": desc, "value": res[0]}
        self.config["config"]["idp"] = {
            "desc": CONFIG_TAGS['idp'],
            "value": True if "[idp]" in self.config["config"]["count"]["value"]
            else False
        }
        self.config["config"]["count"]["value"] = \
            self.config["config"]["count"]["value"].replace("[idp]", "")
        self.print_config()

    def print_config(self):
        for key, val in self.config.items():
            print(f"\t{key.upper()}: {val}")

    def check_signature(self):
        raise NotImplementedError

    def decode(self):
        print(f"[+] Reading the file ({self.filename})")
        self.read_file()
        print(f"[+] Extracting the configuration...")
        self.extract_config()
        self.parse_config()
        print("[+] Done. Final result :")
        for key, val in self.config["config"].items():
            print(f'\t[{key}] ({val["desc"]}) : {val["value"]}')

        return json.dumps(self.config).encode('utf-8')
