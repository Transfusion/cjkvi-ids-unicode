from cjkvi_ids_unicode.data_access.EntityResolver import EntityResolver


class JISX0212(EntityResolver):
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
            if not len(entry[0]):
                continue
            self.map[entry[0][2:]] = chr(int(entry[1][2:], 16))
        t.close()

    def resolve(self, code: str):
        """Code is 4 hex digits. Follows the logic in the header of jisx0212-1990.txt; CHISE uses the HD-JB prefix - see Possibilities of integration between a glyph-image database for Kanji characters and a character ontology. 守岡 知彦. Tomohiko Morioka"""
        return self.map.get(code, None)
