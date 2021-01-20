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
MOJIJOUHOUKIBAN_INFO = "rawdata/mj/IVD_Sequences.txt"

# standard is unchanging, hence no need to fetch...
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

UNRESOLVED_FILE_PREFIX = "UNRESOLVED_"
RESOLVED_FILE_PREFIX = "RESOLVED_"
ENTITIES_RESOLVED_FILE_PREFIX = "ENTITIES_RESOLVED_"
# unresolvable is for all characters that have stroke placeholders or
# DON'T have all of their entity references resolved
UNRESOLVABLE_FILE_PREFIX = "UNRESOLVABLE_"
# partially resolved is for characters with *at least one* entity reference
# resolved, but not all (only append ids which aren't totally unresolved)
ENTITIES_PARTIALLY_RESOLVED_FILE_PREFIX = "ENTITIES_PARTIALLY_RESOLVED_"

MANUALLY_RESOLVED_FILE_PREFIX = "MANUALLY_RESOLVED_"
MANUALLY_PARTIALLY_RESOLVED_FILE_PREFIX = "MANUALLY_PARTIALLY_RESOLVED_"
