from cjkvi_ids_unicode.data_access.EntityResolver import EntityResolver


class JISX0213(EntityResolver):
    def __init__(self, input_file_path):
        self.input_file_path = input_file_path
        self.map = {}
        t = open(self.input_file_path)
        while True:
            line = t.readline()
            if line.startswith("#"):
                continue
            if not line:
                break
            entry = line.split("\t")
            if "+" in entry[1][2:] or not len(entry[1]):
                continue
            self.map[entry[0]] = chr(int(entry[1][2:], 16))
        t.close()

    def resolve(self, plane: int, code: str):
        """Plane follows the logic in the header of jisx0213-2004-std.txt; CHISE uses JX1-, JX2-, and JX3- prefixes. https://www.jstage.jst.go.jp/article/jjadh/1/1/1_86/_pdf """
        return self.map.get(f"{plane+2}-{code.upper()}", None)
