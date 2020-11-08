import unittest

from mozitools.unpacker import *

SAMPLE_HASH = "8f3a5bc6088b999d50bce0eef02c41860bc8ac5e63a2379508c20a1c188eb38d"


class TestUnpacker(unittest.TestCase):
    def test_unpack_sample(self):
        u = MoziUnpacker("/tmp/mozi-decoder-test/Mozi.m")
        self.assertEqual(u.unpack(), "/tmp/mozi-decoder-test/" + SAMPLE_HASH)

    def test_unpack_non_upx_file(self):
        u = MoziUnpacker("/tmp/mozi-decoder-test/NotAnUPXFile")
        self.assertRaises(MoziNotAnUPXFileError, u.unpack)

    def test_unpack_broken_upx(self):
        u = MoziUnpacker("/tmp/mozi-decoder-test/BrokenUPX")
        self.assertRaises(MoziUnknownFormatError, u.unpack)


if __name__ == '__main__':
    unittest.main()
