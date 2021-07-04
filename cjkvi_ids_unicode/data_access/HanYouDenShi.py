from cjkvi_ids_unicode.data_access.EntityResolver import EntityResolver


class HanYouDenShi(EntityResolver):
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
            entry = line.split(" ")
            self.map[entry[-1].strip()] = chr(int(entry[0], 16))
        t.close()

    def resolve(self, entity_reference: str):
        return self.map.get(entity_reference, None)
