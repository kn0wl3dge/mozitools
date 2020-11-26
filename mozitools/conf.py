# Header used to check if it's an UPX file
UPX_STRING = b"UPX!"

# Header used to find the config offset ([ss] after unxor)
CONFIG_HEADER = b"\x15\x15\x29\xD2"

# Size of every element in the config space
CONFIG_SIZE = 428
SIGNATURE1_SIZE = 96
SIGNATURE2_SIZE = 96
CONFIG_VERSION_SIZE = 4
CONFIG_TOTAL_SIZE = CONFIG_SIZE + \
                    SIGNATURE1_SIZE + \
                    SIGNATURE2_SIZE + \
                    CONFIG_VERSION_SIZE

# Hardcoded XOR key used to encrypt the config
XOR_KEY = b"\x4E\x66\x5A\x8F\x80\xC8\xAC\x23\x8D\xAC\x47\x06\xD5\x4F\x6F\x7E"

# The first signature public key used to authenticate the encrypted config
SIGNATURE1_KEY = "\x02\xc0\xa1\x43\x78\x53\xbe\x3c\xc4\xc8\x0a\x29\xe9\x58" \
                 "\xbf\xc6\xa7\x1b\x7e\xab\x72\x15\x1d\x64\x64\x98\x95\xc4" \
                 "\x6a\x48\xc3\x2d\x6c\x39\x82\x1d\x7e\x25\xf3\x80\x44\xf7" \
                 "\x2d\x10\x6b\xcb\x2f\x09\xc6"

# The second signature public key used to authenticate the decrypted config
SIGNATURE2_KEY = "\x02\xd5\xd5\xe7\x41\xee\xdc\xc8\x10\x6d\x2f\x48\x0d\x04" \
                 "\x12\x21\x27\x39\xc7\x45\x0d\x2a\xd1\x40\x72\x01\xd1\x8b" \
                 "\xcd\xc4\x16\x65\x76\x57\xc1\x9d\xe9\xbb\x05\x0d\x3b\xcf" \
                 "\x6e\x70\x79\x60\xf1\xea\xef"

# All tags that can be present in a Mozi config
CONFIG_TAGS = {
    "ss":	"Bot role",
    "ssx": "enable/disable tag [ss]",
    "cpu": "CPU architecture",
    "cpux": "enable/disable tag [cpu]",
    "nd": "new DHT node",
    "hp": "DHT node hash prefix",
    "atk": "DDoS attack type",
    "ver": "Value in V section in DHT protcol",
    "sv": "Update config",
    "ud": "Update bot",
    "dr": "Download and execute payload from the specified URL",
    "rn": "Execute specified command",
    "dip": "ip:port to download Mozi bot",
    "idp": "report bot",
    "count": "URL that used to report bot"
}

# List of the bootstrap nodes hardcoded in Mozi
BOOTSTRAP_NODES = [
    ("router.bittorrent.com", 6881),
    ("dht.transmissionbt.com", 6881),
    ("router.utorrent.com", 6881),
    ("bttracker.debian.org", 6881),
    ("212.129.33.59", 6881),
    ("82.221.103.244", 6881),
    ("130.239.18.159", 6881),
    ("87.98.162.88", 6881),
]

# ELK Settings to import Mozi configurations
ELK_HOSTS = "https://admin:admin@opendistro-opendistro-es-client-service " \
            ".monitoring.svc.cluster.local:9200"
ELK_SSL = True
ELK_INDEX = "mozitools"
ELK_BULK_SIZE = 100

NODES_CACHE_SIZE = 10000
