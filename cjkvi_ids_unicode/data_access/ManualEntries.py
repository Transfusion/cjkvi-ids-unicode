import os


class ManualEntries:
    """IDS entries in the format of https://gitlab.chise.org/CHISE can be manually added to the system and will make it into the output"""

    def __init__(self, input_file_path):
        self.input_file_path = input_file_path
        self.map = {}
        if not os.path.exists(input_file_path):
            return
        t = open(self.input_file_path)
        while True:
            line = t.readline()
            if line.startswith("#"):
                continue
            if not line:
                break
            entry = line.split("\t")
            self.map[entry[1]] = list(map(lambda x: x.strip(), entry[2:]))
        t.close()

    def get_ids(self, char):  # could be partial
        """Gets a list of IDS strings or an empty list if not present."""
        return self.map.get(char, [])
