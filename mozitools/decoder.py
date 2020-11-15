import json
import logging
import re

from mozitools.conf import *


class MoziConfigNotFoundError(Exception):
    """Raised when the decoder can't find the config of the sample."""


class MoziConfigParsingError(Exception):
    """Raised when the decoder is not able to parse the config of the sample."""


def decrypt_config(data):
    data = list(data)
    for i in range(len(data)):
        data[i] ^= XOR_KEY[i % len(XOR_KEY)]
    return ''.join(map(chr, data))


class MoziConfigDecoder:
    def __init__(self, data):
        self.logger = logging.getLogger("mozitools")
        self.config = {}
        self.data = data

    def extract_config(self):
        begin = 0
        end = CONFIG_SIZE
        try:
            self.config["raw_config"] = decrypt_config(self.data[begin:end])
            begin = end
            end += SIGNATURE1_SIZE
            self.config["signature1"] = self.data[begin:end].hex()
            begin = end
            end += CONFIG_VERSION_SIZE
            self.config["version"] = int.from_bytes(
                self.data[begin:end],
                'little'
            )
            begin = end
            end += SIGNATURE2_SIZE
            self.config["signature2"] = self.data[begin:end].hex()
            self.config["config"] = {}
            assert end == CONFIG_TOTAL_SIZE
        except IndexError:
            raise MoziConfigParsingError

    def parse_config(self):
        self.logger.info("[+] Parsing the configuration...")

        for tag, desc in CONFIG_TAGS.items():
            regex = re.compile(rf'\[{tag}\](.*)\[/{tag}\]')
            res = regex.findall(self.config["raw_config"])
            if len(res) != 0:
                self.config["config"][tag] = res[0]
        self.config["config"]["idp"] = True if "[idp]" in self.config[
            "config"]["count"] else False
        self.config["config"]["count"] = \
            self.config["config"]["count"].replace("[idp]", "")
        self.print_config()

    def print_config(self):
        for key, val in self.config.items():
            self.logger.info(f"\t{key.upper()} : {val}")

    def decode(self):
        self.extract_config()
        self.parse_config()
        return self.config


class MoziDecoder:
    """
    This class is used to decode Mozi v2 sample
    Example:
        d = MoziDecoder(unpacked_filename)
        decoded_config = d.decode()
    """
    def __init__(self, filename):
        self.logger = logging.getLogger("mozitools")
        self.filename = filename
        self.data = None
        self.config = {}

    def read_file(self):
        with open(self.filename, 'rb') as fd:
            self.data = fd.read()

    def check_signature(self):
        raise NotImplementedError

    def extract_config(self):
        config_index = self.data.index(CONFIG_HEADER)
        if config_index == -1:
            raise MoziConfigNotFoundError
        self.logger.info(f"[+] Found config at offset: ({hex(config_index)})")
        raw_cfg = self.data[config_index:config_index + CONFIG_TOTAL_SIZE]
        return MoziConfigDecoder(raw_cfg).decode()

    def decode(self):
        self.logger.info(f"[+] Reading the file ({self.filename})")
        self.read_file()
        self.logger.info(f"[+] Extracting the configuration...")
        self.config = self.extract_config()
        self.logger.info("[+] Done. Final result :")
        for key, val in self.config["config"].items():
            self.logger.info(f'\t[{key}] ({CONFIG_TAGS[key]}) : {val}')

        return json.dumps(self.config).encode('utf-8')
