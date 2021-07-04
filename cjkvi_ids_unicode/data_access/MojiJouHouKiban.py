from cjkvi_ids_unicode.data_access.EntityResolver import EntityResolver


class MojiJouHouKiban(EntityResolver):
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
            ucs_cp = entry[1][2:]
            if not len(ucs_cp):
                continue
            self.map[entry[0].strip()] = chr(int(ucs_cp, 16))
        t.close()

    def resolve(self, entity_reference: str):
        return self.map.get(entity_reference, None)
