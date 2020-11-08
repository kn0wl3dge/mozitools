import argparse

from mozitools.decoder import MoziDecoder
from mozitools.unpacker import MoziUnpacker


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="sample file that should be "
                                             "unpacked / decoded",
                        type=str, required=True)
    parser.add_argument("-o", "--output", help="output directory for the \
            unpacked sample", type=str, default="")
    parser.add_argument("-j", "--json", help="dump the config in a json file",
                        action="store_true")
    args = parser.parse_args()

    try:
        u = MoziUnpacker(args.file)
        output_file = u.unpack()
    except Exception as e:
        print("[-] Unpacker failed. Maybe the binary isn't packed.")
        output_file = args.file
    try:
        d = MoziDecoder(output_file)
        config = d.decode()
    except Exception as e:
        print("[-] This doesn't seem to be a Mozi malware sample.")
        config = None

    return config


if __name__ == "__main__":
    main()
