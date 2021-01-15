from ..ui.settings import HyaraGUI
import cutter
import hashlib
import pefile


class HyaraCutter(HyaraGUI):
    def __init__(self):
        super(HyaraCutter, self).__init__()

    def get_disasm(self, start_address, end_address) -> list:
        result = []
        start = int(start_address, 16)
        end = int(end_address, 16)
        while start <= end:
            cutter_data = cutter.cmdj("aoj @ " + str(start))
            result.append(cutter_data[0]["disasm"])
            start += cutter_data[0]["size"]
        return result

    def get_hex(self, start_address, end_address) -> list:
        result = []
        start = int(start_address, 16)
        end = int(end_address, 16)
        while start <= end:
            cutter_data = cutter.cmdj("aoj @ " + str(start))
            result.append(cutter_data[0]["bytes"])
            start += cutter_data[0]["size"]
        return result

    def get_filepath(self) -> str:
        return cutter.cmdj("ij")["core"]["file"]

    def get_md5(self) -> str:
        return hashlib.md5(open(self.get_filepath(), "rb").read()).hexdigest()

    def get_imphash(self) -> str:
        return pefile.PE(self.get_filepath()).get_imphash()

    def get_rich_header(self) -> str:
        rich_header = pefile.PE(self.get_filepath()).parse_rich_header()
        return hashlib.md5(rich_header["clear_data"]).hexdigest()

    def jump_to(self, addr):
        return cutter.cmdj("s " + str(addr))