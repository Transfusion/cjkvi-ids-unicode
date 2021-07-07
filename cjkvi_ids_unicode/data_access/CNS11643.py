from cjkvi_ids_unicode.data_access.EntityResolver import EntityResolver


class CNS11643(EntityResolver):
    def __init__(self, cns11643_file_paths: dict[int, str]):
        self.input_file_paths = cns11643_file_paths
        self.map = {}
        for plane in cns11643_file_paths:
            t = open(cns11643_file_paths[plane])
            while True:
                line = t.readline()
                if line.startswith("#"):
                    continue
                if not line:
                    break
                entry = line.split("\t")
                try:
                    self.map[entry[0]] = chr(int(entry[1].strip()[2:], 16))
                except Exception:
                    pass
            t.close()

    def resolve(self, entity_reference: str):
        return self.map.get(entity_reference, None)
