import cjkvi_ids_unicode.entity_ref_constants as entity_ref_constants

RAW_DATA_DIR = "rawdata"
OUTPUT_DIR = "output"
KAWABATA_IDS_AB = "rawdata/cjkvi-ids/ids.txt"
KAWABATA_IDS_CDEF = "rawdata/cjkvi-ids/ids-ext-cdef.txt"

CHISE_IDS_ROOT_FOLDER = "rawdata/ids"
CHISE_IDS_UCS_PREFIX = "IDS-UCS"

GLYPHWIKI_ROOT_FOLDER = "rawdata/glyphwiki"
GLYPHWIKI_NEWEST_DUMP_NAME = "dump_newest_only.txt"
GLYPHWIKI_VARIANT_INFO = f"rawdata/glyphwiki/{GLYPHWIKI_NEWEST_DUMP_NAME}"

DAIKANWA_ROOT_FOLDER = "rawdata/daikanwa"
DAIKANWA_UCS_INFO = "rawdata/daikanwa/daikanwa-ucs.txt"

MOJIJOUHOUKIBAN_ROOT_FOLDER = "rawdata/mj"
# MOJIJOUHOUKIBAN_INFO = "rawdata/mj/IVD_Sequences.txt"
MOJIJOUHOUKIBAN_INFO = "rawdata/mj/mji.00601_taiou_ucs.txt"

# standard is unchanging, hence no need to fetch...
JISX0208_INFO = "rawdata/jis/jisx0208-1990.txt"
JISX0212_INFO = "rawdata/jis/jisx0212-1990.txt"
JISX0213_INFO = "rawdata/jis/jisx0213-2004-std.txt"

# standard is obsolete, hence no need to fetch...
HANYOUDENSHI_ROOT_FOLDER = "rawdata/hd"
HANYOUDENSHI_INFO = "rawdata/hd/Hanyo-Denshi_20120302_13045.txt"

CNS11643_ROOT_FOLDER = "rawdata/xemacs-chise/etc/char-data"

CNS11643_INFO = {
    1: CNS11643_ROOT_FOLDER + "/" + "C1-to-UCS.txt",
    2: CNS11643_ROOT_FOLDER + "/" + "C2-to-UCS.txt",
    3: CNS11643_ROOT_FOLDER + "/" + "C3-to-UCS.txt",
    4: CNS11643_ROOT_FOLDER + "/" + "C4-to-UCS.txt",
    5: CNS11643_ROOT_FOLDER + "/" + "C5-to-UCS.txt",
    6: CNS11643_ROOT_FOLDER + "/" + "C6-to-UCS.txt",
    7: CNS11643_ROOT_FOLDER + "/" + "C7-to-UCS.txt",
}

MANUAL_IDS_ROOT_FOLDER = "rawdata/manual_ids"

ORIGINAL_FILE_PREFIX = "ORIGINAL_"
# UNRESOLVED_FILE_PREFIX = "UNRESOLVED_"
RESOLVED_FILE_PREFIX = "RESOLVED_"
PARTIALLY_RESOLVED_FILE_PREFIX = "PARTIALLY_RESOLVED_"

ENTITIES_REPLACED_FILE_NAME_TEMPLATE = (
    "ENTITIES_REPLACED_{}.json"  # good for debugging...
)

NO_FULL_RESOLUTION_FILE_NAME_TEMPLATE = (
    "NO_FULL_RESOLUTION_{}.json"  # good for debugging...
)

# ENTITIES_RESOLVED_FILE_PREFIX = "ENTITIES_RESOLVED_"
# entries in unresolvable are for ids strings which have stroke placeholders
# or remaining entity references of characters even after resolution attempt
# therefore, a character may be present in all 3 of
# entities_resolved, unresolvable, and entities_partially_resolved
# UNRESOLVABLE_FILE_PREFIX = "UNRESOLVABLE_"
# partially resolved is for ids which aren't totally unresolved
# i.e. which have some improvement over the original
# ENTITIES_PARTIALLY_RESOLVED_FILE_PREFIX = "ENTITIES_PARTIALLY_RESOLVED_"

# MANUALLY_RESOLVED_FILE_PREFIX = "MANUALLY_RESOLVED_"
# MANUALLY_PARTIALLY_RESOLVED_FILE_PREFIX = "MANUALLY_PARTIALLY_RESOLVED_"

# TOTALLY_UNRESOLVABLE_FILE_PREFIX = "TOTALLY_UNRESOLVABLE_"

OUTPUT_METADATA_JSON_NAME = "metadata.json"
OUTPUT_METADATA_JSON = "output/" + OUTPUT_METADATA_JSON_NAME
HTML_TEMPLATE_DIR = "html_template"


STROKE_PLACEHOLDERS = set(
    [
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "11",
        "①",
        "②",
        "③",
        "④",
        "⑤",
        "⑥",
        "⑦",
        "⑧",
        "⑨",
        "⑩",
        "⑪",
        "⑫",
        "⑬",
        "⑭",
        "⑮",
        "⑯",
        "⑰",
        "⑱",
        "⑲",
        "⑳",
    ]
)
