import typing, datetime, json
from collections import namedtuple
from cjkvi_ids_unicode.types import CharIDSTuple

# this is a type
from cjkvi_ids_unicode.driver import CharIDSTuple
import cjkvi_ids_unicode.constants as constants


class MetadataGenerator:
    Entry = namedtuple(
        "Entry",
        "filename resolved_cnt entities_resolved_cnt partially_resolved_cnt manually_resolved_cnt manually_partially_resolved_cnt totally_unresolvable_cnt resolved_entries entities_resolved_entries manually_resolved_entries partially_resolved_entries manually_partially_resolved_entries unresolved_entries unresolvable_entries original_total",
    )

    def __init__(self):
        self.map = {}

    def add_ids_data(
        self,
        filename: str,
        chars: typing.Iterable,
        resolved: list[CharIDSTuple],  # list of tuple of char, [ids]
        unresolved: list[CharIDSTuple],  # list of tuple of char, [ids] (ids from CHISE)
        entities_resolved: list[
            CharIDSTuple
        ],  # list of tuple of char, [ids] (lost structural information)
        unresolvable: list[CharIDSTuple],  # list of tuple of char, [ids]
        partially_resolved: list[CharIDSTuple],
        manually_resolved: list[CharIDSTuple],
        manually_partially_resolved: list[CharIDSTuple],
    ):
        resolved_map = {}
        for (char, ids) in resolved:
            resolved_map[char] = ids

        entities_resolved_map = {}
        for (char, ids) in entities_resolved:
            entities_resolved_map[char] = ids

        manually_resolved_map = {}
        for (char, ids) in manually_resolved:
            manually_resolved_map[char] = ids

        partially_resolved_map = {}
        for (char, ids) in partially_resolved:
            partially_resolved_map[char] = ids

        manually_partially_resolved_map = {}
        for (char, ids) in manually_partially_resolved:
            manually_partially_resolved_map[char] = ids

        # not used in stats calculation
        unresolved_map = {}
        for (char, ids) in unresolved:
            unresolved_map[char] = ids

        unresolvable_map = {}
        for (char, ids) in unresolvable:
            unresolvable_map[char] = ids

        resolved_cnt = 0
        entities_resolved_cnt = 0
        partially_resolved_cnt = 0
        manually_resolved_cnt = 0
        manually_partially_resolved_cnt = 0
        # computed below, don't conflate with the unresolvable_ file
        totally_unresolvable_cnt = 0

        for char in chars:
            if char in resolved_map:
                resolved_cnt += 1
            elif char in entities_resolved_map:
                entities_resolved_cnt += 1
            elif char in manually_resolved_map:
                manually_resolved_cnt += 1
            elif char in partially_resolved_map:
                partially_resolved_cnt += 1
            elif char in manually_partially_resolved_map:
                manually_partially_resolved_cnt += 1
            else:
                totally_unresolvable_cnt += 1

        # the raw number of entries in the respective maps
        resolved_entries = len(resolved_map)
        entities_resolved_entries = len(entities_resolved_map)
        manually_resolved_entries = len(manually_resolved_map)
        partially_resolved_entries = len(partially_resolved_map)
        manually_partially_resolved_entries = len(manually_partially_resolved_map)
        # including the two files that aren't used in stats calculation
        unresolved_entries = len(unresolved_map)
        unresolvable_entries = len(unresolvable_map)

        self.map[filename] = MetadataGenerator.Entry(
            filename,
            resolved_cnt,
            entities_resolved_cnt,
            partially_resolved_cnt,
            manually_resolved_cnt,
            manually_partially_resolved_cnt,
            totally_unresolvable_cnt,
            # raw entries
            resolved_entries,
            entities_resolved_entries,
            manually_resolved_entries,
            partially_resolved_entries,
            manually_partially_resolved_entries,
            # two files that aren't used in stats calculation
            unresolved_entries,
            unresolvable_entries,
            len(chars),
        )

    def generate_html(self):
        pass

    def write_output_metadata_json(self):
        j = {}

        for filename in self.map:
            j[filename] = {
                "original_file": constants.ORIGINAL_FILE_PREFIX + filename,
                "resolved_file": constants.RESOLVED_FILE_PREFIX + filename,
                "entities_resolved_file": constants.ENTITIES_RESOLVED_FILE_PREFIX
                + filename,
                "entities_partially_resolved_file": constants.ENTITIES_PARTIALLY_RESOLVED_FILE_PREFIX
                + filename,
                "manually_resolved_file": constants.MANUALLY_RESOLVED_FILE_PREFIX
                + filename,
                "manually_partially_resolved_file": constants.MANUALLY_PARTIALLY_RESOLVED_FILE_PREFIX
                + filename,
                # the 2 unresolved not used in stats calculation
                "unresolved_file": constants.UNRESOLVED_FILE_PREFIX + filename,
                "unresolvable_file": constants.UNRESOLVABLE_FILE_PREFIX + filename,
                "metadata": self.map[filename]._asdict(),
            }
        j["ts"] = datetime.datetime.now().isoformat()

        with open(constants.OUTPUT_METADATA_JSON, "w") as outfile:
            json.dump(j, outfile)
