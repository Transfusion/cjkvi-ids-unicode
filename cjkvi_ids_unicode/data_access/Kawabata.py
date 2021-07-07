from cjkvi_ids_unicode.utils import is_valid_ids
from . import BaseSource


class Kawabata(BaseSource):
    """Reads files in the format of https://github.com/cjkvi/cjkvi-ids/"""

    def __init__(self, input_file_path):
        self.input_file_path = input_file_path
        self.map = {}
        t = open(self.input_file_path)
        while True:
            line = t.readline()
            if line.startswith(";") or line.startswith("#"):
                continue
            if not line:
                break

            split = list(map(lambda x: x.strip(), line.split("\t")))
            char, ids = chr(int(split[0][2:], 16)), split[2:]
            self.map[char] = ids
        t.close()

    def get_all_ids(self, char):
        return self.map.get(char, [])

    def get_valid_ids(self, char):
        if char not in self.map:
            return []
        else:
            return list(filter(lambda x: is_valid_ids(x), self.map[char]))
