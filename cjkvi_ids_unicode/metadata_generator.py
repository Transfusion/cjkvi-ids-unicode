from cjkvi_ids_unicode.types import CharIDSTuple, IDSDict
import typing, datetime, json, os
from shutil import copyfile
from collections import namedtuple

# this is a type
import cjkvi_ids_unicode.constants as constants
from jinja2 import Environment, FileSystemLoader


class MetadataGenerator:

    Entry = namedtuple(
        "Entry",
        "filename resolved_cnt partially_resolved_cnt, no_full_resolution_cnt original_total",
    )

    def __init__(self):
        self.map = {}

    def add_ids_data(
        self,
        filename: str,
        chars: typing.Iterable,
        resolved: list[CharIDSTuple],  # list of tuple of char, [ids]
        partially_resolved: list[CharIDSTuple],
        no_full_resolution_map: IDSDict,
    ):
        resolved_cnt = len(resolved)
        partially_resolved_cnt = len(partially_resolved)
        no_full_resolution_cnt = len(no_full_resolution_map)

        self.map[filename] = MetadataGenerator.Entry(
            filename,
            resolved_cnt,
            partially_resolved_cnt,
            no_full_resolution_cnt,
            len(chars),
        )

    def get_metadata(self):
        j = {"ids_data": {}}

        for filename in sorted(self.map.keys()):
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

            j["ids_data"][filename]["resolved"] = {
                "file": constants.RESOLVED_FILE_PREFIX + filename,
                "size": os.path.getsize(
                    os.path.join(
                        constants.OUTPUT_DIR, constants.RESOLVED_FILE_PREFIX + filename
                    )
                ),
                "entries": self.map[filename].resolved_cnt,
            }

            j["ids_data"][filename]["partially_resolved"] = {
                "file": constants.PARTIALLY_RESOLVED_FILE_PREFIX + filename,
                "size": os.path.getsize(
                    os.path.join(
                        constants.OUTPUT_DIR, constants.RESOLVED_FILE_PREFIX + filename
                    )
                ),
                "entries": self.map[filename].partially_resolved_cnt,
            }

            stripped_file_name = os.path.splitext(filename)[0]
            j["ids_data"][filename]["no_full_resolution"] = {
                "file": constants.NO_FULL_RESOLUTION_FILE_NAME_TEMPLATE.format(
                    stripped_file_name
                ),
                "size": os.path.getsize(
                    os.path.join(
                        constants.OUTPUT_DIR,
                        constants.NO_FULL_RESOLUTION_FILE_NAME_TEMPLATE.format(
                            stripped_file_name
                        ),
                    )
                ),
                "entries": self.map[filename].no_full_resolution_cnt,
            }

            # for field in MetadataGenerator.RAW_FILE_METADATA_FIELDS:
            #     if getattr(self.map[filename], field + "_entries"):
            #         j["ids_data"][filename][field] = {
            #             "file": MetadataGenerator.RAW_FILE_METADATA_FIELDS[field]
            #             + filename,
            #             "size": os.path.getsize(
            #                 os.path.join(
            #                     constants.OUTPUT_DIR,
            #                     MetadataGenerator.RAW_FILE_METADATA_FIELDS[field]
            #                     + filename,
            #                 )
            #             ),
            #             "entries": getattr(self.map[filename], field + "_entries"),
            #         }

            # internal_dict = self.map[filename]._asdict()
            # for key in list(internal_dict.keys()):
            #     if key.endswith("entries"):
            #         del internal_dict[key]

            # j["ids_data"][filename]["metadata"] = internal_dict

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
                "g_pc": "{0:.2f}".format(
                    100
                    * self.map[filename].resolved_cnt
                    / self.map[filename].original_total
                ),
                "ng_pc": "{0:.2f}".format(
                    100
                    * self.map[filename].no_full_resolution_cnt
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
