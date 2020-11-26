import argparse
import logging

from mozitools.decoder import MoziDecoder
from mozitools.tracker import MoziTracker
from mozitools.unpacker import MoziUnpacker


HEADER = """
                             __                   ___             
 /'\_/`\                  __/\ \__               /\_ \            
/\      \    ___   ____  /\_\ \ ,_\   ___     ___\//\ \     ____  
\ \ \__\ \  / __`\/\_ ,`\\\\/\ \ \ \/  / __`\  / __`\\\\ \ \   /',__\ 
 \ \ \_/\ \/\ \L\ \/_/  /_\ \ \ \ \_/\ \L\ \/\ \L\ \\\\_\ \_/\__, `\\
  \ \_\\\\ \_\ \____/ /\____\\\\ \_\ \__\ \____/\ \____//\____\/\____/
   \/_/ \/_/\/___/  \/____/ \/_/\/__/\/___/  \/___/ \/____/\/___/ 
                                                                  
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--decode', help="decode a mozi packed file and"
                                               " extract it's configuration",
                        action="store_true")
    parser.add_argument('-t', '--tracker', help="fake mozi node to identify "
                                                "mozi node and configurations",
                        action="store_true")

    parser.add_argument("-f", "--file", help="sample file that should be "
                                             "unpacked / decoded",
                        type=str)
    parser.add_argument("-o", "--output", help="output directory if different "
                                             "from the sample",
                        type=str)
    parser.add_argument("-j", "--json", help="dump the config in a json file",
                        action="store_true")
    parser.add_argument("-q", "--quiet", help="don't output any log",
                        action="store_true")

    logger = logging.getLogger("mozitools")
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    logger.addHandler(stream_handler)

    logger.info(HEADER)

    args = parser.parse_args()
    if args.quiet:
        logger.disabled = True

    if args.decode and args.file != "":
        logger.info("[+] Starting the Unpacker")
        try:
            if args.output:
                u = MoziUnpacker(args.file, args.output)
            else:
                u = MoziUnpacker(args.file)
            output_file = u.unpack()
        except Exception as e:
            logger.error("[-] Unpacker failed. Maybe the binary isn't packed.")
            output_file = args.file
        try:
            logger.info("[+] Starting the Decoder")
            d = MoziDecoder(output_file)
            config = d.decode()
        except Exception as e:
            logger.error("[-] This doesn't seem to be a Mozi malware sample.")
            config = None
        if config and args.json:
            with open(output_file + "-config.json", 'wb') as fd:
                fd.write(config)
    elif args.tracker:
        logger.info("[+] Starting Tracker")
        s = MoziTracker()
        s.start()
        s.find_nodes()
        s.join()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
