import argparse
import json
import logging
from sys import path

from mozitools.decoder import MoziDecoder
from mozitools.tracker import MoziTracker
from mozitools.unpacker import MoziUnpacker


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--decode', help="decode a mozi packed file and"
                                               " extract it's configuration",
                        action="store_true")
    parser.add_argument('-t', '--tracker', help="fake a mozi node to search "
                                                "mozi node and configurations",
                        action="store_true")

    parser.add_argument("-f", "--file", help="sample file that should be "
                                             "unpacked / decoded",
                        type=str)
    parser.add_argument("-o", "--output", help="output directory for the \
            unpacked sample", type=str, default="")
    parser.add_argument("-j", "--json", help="dump the config in a json file",
                        action="store_true")
    parser.add_argument("-q", "--quiet", help="don't output any log",
                        action="store_true")
    args = parser.parse_args()

    logger = logging.getLogger("mozitools")
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    logger.addHandler(stream_handler)

    if args.quiet:
        logger.disabled = True

    if args.decode and args.file != "":
        logger.info("[+] Starting Decoder")
        try:
            u = MoziUnpacker(args.file)
            output_file = u.unpack()
        except Exception as e:
            logger.error("[-] Unpacker failed. Maybe the binary isn't packed.")
            output_file = args.file
        try:
            logger.info("[+] Starting Unpacker")
            d = MoziDecoder(output_file)
            config = d.decode()
        except Exception as e:
            logger.error("[-] This doesn't seem to be a Mozi malware sample.")
            config = None
        if config:
            with open(path.dirname(args.file) + "/mozi-config.json") as fd:
                fd.write(json.dumps(config))

    if args.tracker:
        logger.info("[+] Starting Tracker")
        s = MoziTracker(10000)
        s.start()
        s.find_nodes()
        s.join()


if __name__ == "__main__":
    main()
