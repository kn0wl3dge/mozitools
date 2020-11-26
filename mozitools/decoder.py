import json
import logging
import re

from mozitools.conf import XOR_KEY, CONFIG_TOTAL_SIZE, CONFIG_SIZE, \
    SIGNATURE1_SIZE, CONFIG_VERSION_SIZE, SIGNATURE2_SIZE, CONFIG_TAGS, \
    CONFIG_HEADER


class MoziConfigNotFoundError(Exception):
    """Raised when the decoder can't find the config of the sample."""


class MoziConfigParsingError(Exception):
    """Raised when the decoder is not able to parse the config of the sample."""


def decrypt_config(data):
    """
    Decrypt the Mozi configuration using a simple XOR algorithm with an
    hardcoded key stored in conf.py
    :param data: config being decrypted
    :return: decrypted config
    """
    data = list(data)
    for i in range(len(data)):
        data[i] ^= XOR_KEY[i % len(XOR_KEY)]
    return ''.join(map(chr, data))


class MoziConfigDecoder:
    """
        This class is used to decrypt and parse a Mozi configuration.
        Example:
            d = MoziConfigDecoder(my_config)
            config = d.decode()
    """
    def __init__(self, data):
        """
        Init a decoder object.
        :param data: encrypted Mozi configuration
        """
        self.logger = logging.getLogger("mozitools")
        self.config = {}
        self.data = data

    def extract_config(self):
        """
        Extract and store the different fields of a Mozi configuration such
        as raw configurations, versions and signatures.
        """
        begin = 0
        end = CONFIG_TOTAL_SIZE
        try:
            self.config["raw_config"] = decrypt_config(self.data[begin:end])
            begin = CONFIG_SIZE
            end = begin + SIGNATURE1_SIZE
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
        """
        Parse the known configuration tags defined in conf.py. Basically, the
        raw configuration looks like "[ss]Something[/ss][dip]Something[/dip]..."
        :return:
        """
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
        self.config["raw_config"] = self.config["raw_config"][:CONFIG_SIZE]\
            .rstrip('\x00')
        self.print_config()

    def print_config(self):
        """
        Print the different tags extracted during the parsing step.
        """
        for key, val in self.config.items():
            if key != "raw_config":
                self.logger.info(f"\t{key.upper()} : {val}")
        self.logger.info("\n=======>")
        for key, val in self.config["config"].items():
            self.logger.info(f'\t[{key}] ({CONFIG_TAGS[key]}) : {val}')

    def decode(self):
        """
        Extract, decrypt and parse the configuration stored in the object.
        :return: final configuration as a dictionary
        """
        self.extract_config()
        self.parse_config()
        return self.config


class MoziDecoder:
    """
    This class is used to decode Mozi v2 sample
    Example:
        d = MoziDecoder(unpacked_mozi_filename)
        decoded_config = d.decode()
    """
    def __init__(self, filename):
        """
        Init a decoder object.
        :param filename: unpacked Mozi sample
        """
        self.logger = logging.getLogger("mozitools")
        self.filename = filename
        self.data = None
        self.config = {}

    def read_file(self):
        """
        Read the sample and stores it in the object.
        """
        with open(self.filename, 'rb') as fd:
            self.data = fd.read()

    def extract_config(self):
        """
        Find and extract the static configuration hardcoded in the sample.
        :return: decrypted and parsed configuration
        """
        config_index = self.data.index(CONFIG_HEADER)
        if config_index == -1:
            raise MoziConfigNotFoundError
        self.logger.info(f"[+] Found config at offset: ({hex(config_index)})")
        raw_cfg = self.data[config_index:config_index + CONFIG_TOTAL_SIZE]
        return MoziConfigDecoder(raw_cfg).decode()

    def decode(self):
        """
        Extract, decrypt and parse the configuration stored in the object.
        :return: utf-8 string representing the final configuration
        """
        self.logger.info(f"[+] Reading the file ({self.filename})")
        self.read_file()
        self.logger.info(f"[+] Extracting the configuration...")
        self.config = self.extract_config()
        self.logger.info("[+] Done.")

        return json.dumps(self.config).encode('utf-8')
