from uuid import uuid4
from subprocess import run
from hashlib import md5, sha1, sha256, sha512
from os import path

from mozitools.conf import UPX_STRING


class MoziUnknownFormatError(Exception):
    """Raised when the unpacker doesn't understand the file format."""


class MoziNotAnUPXFileError(Exception):
    """
    Raised when the input is not a an UPX file.
    """


class MoziUnpacker:
    """
    This class is used to unpack Mozi v2 sample
    Example:
        u = MoziUnpacker("./Mozi.m")
        unpacked_binary_path = u.unpack()
    """
    def __init__(self, filename, output=""):
        self.filename = filename
        if output != "":
            if output[-1] == "/":
                output = output[:-1]
            self.output = output + "/" + str(uuid4())
        else:
            self.output = path.dirname(self.filename) + "/" + str(uuid4())
        self.data = None

    def read_file(self):
        with open(self.filename, 'rb') as fd:
            self.data = fd.read()

    def compute_hashes(self):
        print("[+] Computing file hashes...")
        hashes = {
            "MD5": md5(self.data).hexdigest(),
            "SHA1": sha1(self.data).hexdigest(),
            "SHA256": sha256(self.data).hexdigest(),
            "SHA512": sha512(self.data).hexdigest()
        }
        for hashtype, val in hashes.items():
            print(f"\t{hashtype}: {val}")
        return hashes

    def check_upx(self):
        # This could be better
        return b"UPX!" in self.data

    def repair_upx_header(self):
        print(f"[+] Editing {self.filename} to repair the p_info struct...")
        try:
            p_filesize = self.data[-12:-8]
            struc_l_info_index = self.data.index(UPX_STRING) - 4
            self.data = self.data[:struc_l_info_index + 16] + 2 * p_filesize + \
                        self.data[struc_l_info_index + 24:]
        except:
            print("[-] Can't repair the header. Possibly an index error.")
            raise MoziUnknownFormatError

    def upx_unpack(self):
        print("[+] Running UPX unpacker...")
        with open(self.output, 'wb') as fd:
            fd.write(self.data)
        res = run(["upx", "-d", self.output],
                  capture_output=True)
        if res.returncode == 0:
            print(res.stdout.decode('utf-8'))
            print(f"[+] Succesfully unpacked {self.filename}")
            with open(self.output, 'rb') as fd:
                self.data = fd.read()
            return res

        print(res.stderr.decode('utf-8'))
        print("[-] Can't unpack the binary using UPX.")
        raise MoziUnknownFormatError

    def unpack(self):
        print(f"[+] Reading the file ({self.filename})")
        self.read_file()
        print("[+] Checking if it's an UPX ELF binary...")
        if not self.check_upx():
            print("[-] Can't find \"UPX!\" string in this file. Maybe not an "
                  "UPX ?")
            raise MoziNotAnUPXFileError()
        self.repair_upx_header()
        self.upx_unpack()
        hashes = self.compute_hashes()
        new_file = path.dirname(self.output) + '/' + hashes["SHA256"]
        run(["mv", self.output, new_file])
        print(f"[+] Unpacked file has been saved as {hashes['SHA256']}")
        print("[!] Be careful ! Do not execute the file !")
        return new_file
