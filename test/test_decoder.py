import unittest

from mozitools.decoder import MoziDecoder
from mozitools.unpacker import MoziUnpacker

SAMPLE_HASH = "8f3a5bc6088b999d50bce0eef02c41860bc8ac5e63a2379508c20a1c188eb38d"
SAMPLE_CONFIG = b"""{"raw_config": "[ss]botv2[/ss][dip]192.168.2.100:80[/dip][hp]88888888[/hp][count]http://ia.51.la/go1?id=17675125&pu=http%3a%2f%2fv.baidu.com/[idp][/count]", "signature1": "b0e74673720d660dd4a369e706576943f6be4f71966516acb1c842d5bf36cfc86717caf562b1fbc12b0a80fab170217ba2aa3e3bad1844af856320add9c1f8afe2eac3acf522c7737d7568551b902b926fd65c969a2c4f34aa4a380fe2ada249", "version": 2, "signature2": "c33f318d0bee9747640f78bbb90b9b4192c325d178e7e50575d67c3566917abee559b6cf1acb5d2bc4db08a420afea4d921a2e6dff86cc92e603ce6987f2f2a100e8408f2c184a53ccb29978bbd16261e964ee7e80aa86296d9880429a31e1cf", "config": {"ss": "botv2", "hp": "88888888", "dip": "192.168.2.100:80", "count": "http://ia.51.la/go1?id=17675125&pu=http%3a%2f%2fv.baidu.com/", "idp": true}}"""


class TestDecoder(unittest.TestCase):
    def test_decode_sample(self):
        u = MoziUnpacker("/tmp/mozi-decoder-test/Mozi.m")
        u.unpack()
        d = MoziDecoder("/tmp/mozi-decoder-test/" + SAMPLE_HASH)
        config = d.decode()
        print(config)
        self.assertEqual(config, SAMPLE_CONFIG)


if __name__ == '__main__':
    unittest.main()
