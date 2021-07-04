# DONE: this class should be relatively testable
from cjkvi_ids_unicode.data_access.EntityResolver import EntityResolver


class GlyphWiki(EntityResolver):
    """Currently mostly intended for resolving CDP- entities."""

    KAGE_FULL_BOUNDING_BOX = "99:0:0:0:0:200:200:"

    class Entry:
        def __init__(self, related, data):
            self.related = related
            self.data = data

        def __repr__(self):
            return f"<{self.related} {self.data}>"

    def __init__(self, input_file_path):
        self.input_file_path = input_file_path
        self.map = {}
        t = open(self.input_file_path)
        while True:
            line = t.readline()
            if (
                line.startswith("     ")
                or line.startswith("-")
                or line.startswith(" abc")
                or line.startswith("(")
            ):
                continue
            if not line:
                break
            entry = map(lambda x: x.strip(), line.split("|"))
            entry = list(entry)
            if len(entry) < 3:
                continue
            self.map[entry[0]] = GlyphWiki.Entry(entry[1], entry[2])
        t.close()

    def resolve(self, entity_reference: str):
        base_entity_reference = entity_reference
        try:
            base_entity_reference = entity_reference[: entity_reference.index("-")]
        except ValueError:
            pass

        if entity_reference not in self.map:
            return None
        entry = self.map[entity_reference]
        if entry.related == "u3013":
            if entry.data.startswith(GlyphWiki.KAGE_FULL_BOUNDING_BOX):
                alias = entry.data[len(GlyphWiki.KAGE_FULL_BOUNDING_BOX) :]
                return self.resolve(alias)
            else:
                return None

        # there is an infinite loop between u5c71-j and u5c71 lol
        elif (
            entry.related == entity_reference or entry.related == base_entity_reference
        ):
            return chr(int(entry.related[1:], 16))
        else:
            return self.resolve(entry.related)
