import logging
import socket
import uuid
import bencodepy
from datetime import datetime
from struct import unpack
from socket import inet_ntoa
from threading import Thread, RLock
from secrets import token_bytes
from elasticsearch import Elasticsearch, helpers

from mozitools.conf import ELK_HOSTS, ELK_INDEX, ELK_SSL, \
    ELK_BULK_SIZE, NODES_CACHE_SIZE, CONFIG_SIZE, BOOTSTRAP_NODES
from mozitools.decoder import MoziConfigDecoder


def mozi_id():
    prefix = "88888888"
    return prefix.encode('ascii') + token_bytes(20 - len(prefix))


def decode_nodes(nodes):
    res = []
    if (len(nodes) % 26) == 0:
        for i in range(0, len(nodes), 26):
            node_id = nodes[i:i + 20]
            ip = inet_ntoa(nodes[i + 20:i + 24])
            port = unpack("!H", nodes[i + 24:i + 26])[0]
            res.append((node_id, ip, port))
    return res


class ELK:
    def __init__(self):
        self.logger = logging.getLogger("mozitools")
        self.es = Elasticsearch(
            hosts=ELK_HOSTS,
            use_ssl=ELK_SSL,
            verify_certs=False,
        )
        self.configs = []

    def send_to_elastic(self):
        try:
            helpers.bulk(self.es, self.configs, index=ELK_INDEX)
            self.logger.info("[+] Success")
        except Exception as e:
            self.logger.error("[-] Something bad happened with Elastic DB")
        self.configs = []

    def add_config(self, config):
        if len(self.configs) == ELK_BULK_SIZE:
            self.logger.info("[+] Sending config to Elastic DB...")
            self.send_to_elastic()
        else:
            self.configs.append(config)


class MoziTracker(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.setDaemon(True)
        self.ufd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,
                                 socket.IPPROTO_UDP)
        self.elk = ELK()
        self.table = DHTTable()
        self.lock = RLock()
        self.logger = logging.getLogger("mozitools")

    def parse_response(self, msg, address):
        try:
            data = msg[b'r'][b'nodes']
        except KeyError:
            return
        if data[:4] == b'\x15\x15)\xd2' and len(data) == 624:
            node_id = msg[b'r'][b'id']
            config = MoziConfigDecoder(data).decode()
            if "config" in config.keys():
                self.logger.info(f"[+] Found a Mozi node at {address}")
                config["config"]["ip_address"] = address[0]
                config["config"]["port"] = address[1]
                config["config"]["node_id"] = node_id.hex()
                config["config"]["raw"] = config["raw_config"]
                config["config"]["timestamp"] = datetime.utcnow()
                config["config"]["_id"] = uuid.uuid4()
                self.elk.add_config(config["config"])
        else:
            nodes = decode_nodes(data)
            self.lock.acquire()
            for node in nodes:
                (node_id, ip, port) = node
                if len(node_id) != 20:
                    continue
                self.table.add(DHTNode(ip, port))
            self.lock.release()

    def send_find_node(self, node, n=1):
        for _ in range(n):
            msg = {
                "t": "1",
                "y": "q",
                "q": "find_node",
                "a": {"id": self.table.my_node_id, "target": mozi_id()},
                "v": "\x44\x42\x1f\x71"
            }
            try:
                self.ufd.sendto(bencodepy.encode(msg), (node.ip, node.port))
            except Exception as e:
                pass

    def find_nodes(self):
        while True:
            for address in BOOTSTRAP_NODES:
                self.send_find_node(
                    DHTNode(address[0], address[1]),
                    n=10
                )

            if len(self.table.nodes) > 0:
                for node in self.table.nodes:
                    self.send_find_node(node)

                self.lock.acquire()
                self.table.nodes = []
                self.lock.release()

    def run(self):
        while True:
            try:
                (data, address) = self.ufd.recvfrom(65536)
                msg = bencodepy.decode(data)
                if msg[b'y'] == b'r':
                    self.parse_response(msg, address)
            except Exception:
                pass


class DHTTable:
    def __init__(self):
        self.my_node_id = mozi_id()
        self.nodes = []
        self.lasts = []

    def add(self, node):
        if node in self.lasts:
            return
        self.nodes.append(node)
        if (node.ip, node.port) not in BOOTSTRAP_NODES:
            self.lasts.append(node)
        if len(self.lasts) > NODES_CACHE_SIZE:
            self.lasts.pop(0)


class DHTNode:
    def __init__(self, ip=None, port=None):
        self.ip = ip
        self.port = port

    def __eq__(self, other):
        if isinstance(other, DHTNode):
            return self.ip == other.ip and self.port == other.port
        return False
