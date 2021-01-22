import typing, datetime, json, os
from shutil import copyfile
from collections import namedtuple

# this is a type
from cjkvi_ids_unicode.driver import CharIDSTuple
import cjkvi_ids_unicode.constants as constants
from jinja2 import Environment, FileSystemLoader


class MetadataGenerator:
    RAW_FILE_METADATA_FIELDS = {
        "resolved": constants.RESOLVED_FILE_PREFIX,
        "entities_resolved": constants.ENTITIES_RESOLVED_FILE_PREFIX,
        "manually_resolved": constants.MANUALLY_RESOLVED_FILE_PREFIX,
        "partially_resolved": constants.ENTITIES_PARTIALLY_RESOLVED_FILE_PREFIX,
        "manually_partially_resolved": constants.MANUALLY_PARTIALLY_RESOLVED_FILE_PREFIX,
        "unresolved": constants.UNRESOLVED_FILE_PREFIX,
        "unresolvable": constants.UNRESOLVABLE_FILE_PREFIX,
        "totally_unresolvable": constants.TOTALLY_UNRESOLVABLE_FILE_PREFIX,
    }

    Entry = namedtuple(
        "Entry",
        "filename resolved_cnt entities_resolved_cnt partially_resolved_cnt manually_resolved_cnt manually_partially_resolved_cnt totally_unresolvable_cnt resolved_entries entities_resolved_entries manually_resolved_entries partially_resolved_entries manually_partially_resolved_entries unresolved_entries unresolvable_entries totally_unresolvable_entries original_total",
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
        totally_unresolvable: list[CharIDSTuple],
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

        totally_unresolvable_map = {}
        for (char, ids) in totally_unresolvable:
            totally_unresolvable_map[char] = ids

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
        # including the three files that aren't used in stats calculation
        unresolved_entries = len(unresolved_map)
        unresolvable_entries = len(unresolvable_map)
        totally_unresolvable_entries = len(totally_unresolvable_map)

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
            totally_unresolvable_entries,
            len(chars),
        )

    def get_metadata(self):
        j = {"ids_data": {}}

        for filename in self.map:
            j["ids_data"][filename] = {}

            j["ids_data"][filename]["original"] = {
                "file": constants.ORIGINAL_FILE_PREFIX + filename,
                "size": os.path.getsize(
                    os.path.join(
                        constants.OUTPUT_DIR, constants.ORIGINAL_FILE_PREFIX + filename
                    )
                ),
                "entries": self.map[filename].original_total,
            }

            for field in MetadataGenerator.RAW_FILE_METADATA_FIELDS:
                if getattr(self.map[filename], field + "_entries"):
                    j["ids_data"][filename][field] = {
                        "file": MetadataGenerator.RAW_FILE_METADATA_FIELDS[field]
                        + filename,
                        "size": os.path.getsize(
                            os.path.join(
                                constants.OUTPUT_DIR,
                                MetadataGenerator.RAW_FILE_METADATA_FIELDS[field]
                                + filename,
                            )
                        ),
                        "entries": getattr(self.map[filename], field + "_entries"),
                    }

            internal_dict = self.map[filename]._asdict()
            for key in list(internal_dict.keys()):
                if key.endswith("entries"):
                    del internal_dict[key]

            j["ids_data"][filename]["metadata"] = internal_dict

        j["ts"] = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%S.%fZ")
        return j

    def generate_html(self):
        self.write_output_metadata_json()

        env = Environment(loader=FileSystemLoader(constants.HTML_TEMPLATE_DIR))
        template = env.get_template("index.html")

        # metadata = self.get_metadata()

        stats = {}
        for filename in self.map:
            stats[filename] = {
                "k_pc": "{0:.2f}".format(
                    100
                    * self.map[filename].resolved_cnt
                    / self.map[filename].original_total
                ),
                "e_pc": "{0:.2f}".format(
                    100
                    * self.map[filename].entities_resolved_cnt
                    / self.map[filename].original_total
                ),
                "m_pc": "{0:.2f}".format(
                    100
                    * self.map[filename].manually_resolved_cnt
                    / self.map[filename].original_total
                ),
                "p_pc": "{0:.2f}".format(
                    100
                    * self.map[filename].partially_resolved_cnt
                    / self.map[filename].original_total
                ),
                "x_pc": "{0:.2f}".format(
                    100
                    * self.map[filename].manually_partially_resolved_cnt
                    / self.map[filename].original_total
                ),
                "u_pc": "{0:.2f}".format(
                    100
                    * self.map[filename].totally_unresolvable_cnt
                    / self.map[filename].original_total
                ),
            }

        rendered = template.render(
            stats=stats,
            complete_metadata=self.get_metadata(),
            metadata_json_name=constants.OUTPUT_METADATA_JSON_NAME,
            metadata_source_cnt=len(self.map),
            metadata_json_size=MetadataGenerator.get_output_metadata_json_size(),
        )
        with open(os.path.join(constants.OUTPUT_DIR, "index.html"), "w") as f:
            f.write(rendered)

        f.close()

        copyfile(
            os.path.join(constants.HTML_TEMPLATE_DIR, "style.css"),
            os.path.join(constants.OUTPUT_DIR, "style.css"),
        )

    def write_output_metadata_json(self):
        j = self.get_metadata()

        with open(constants.OUTPUT_METADATA_JSON, "w") as outfile:
            json.dump(j, outfile, indent=4)

    def get_output_metadata_json_size():
        if os.path.exists(constants.OUTPUT_METADATA_JSON):
            return os.path.getsize(constants.OUTPUT_METADATA_JSON)
        else:
            return None
