import cjkvi_ids_unicode.constants as constants


def convert_cdp_to_glyphwiki_key(entity: str):
    """variants and itaiji
    CDP-i001-86D6 -> cdp-86d6-itaiji-001
    CDP-v001-8851 -> cdp-8851-var-001"""
    if entity[4] == "i":
        entity = (
            constants.entity_ref_constants.CDP_PREFIX
            + entity[9:]
            + "-itaiji-"
            + entity[5:8]
        )
    elif entity[4] == "v":
        entity = (
            constants.entity_ref_constants.CDP_PREFIX
            + entity[9:]
            + "-var-"
            + entity[5:8]
        )
    return entity.lower()


def convert_ucs_to_glyphwiki_key(entity: str):
    """U-v002+4E11 -> u4e11-var-002"""
    if entity[1] == '+':
        entity = 'u' + entity[2:]
    elif entity[2] == "i":
        entity = "u" + entity[7:] + "-itaiji-" + entity[3:6]
    elif entity[2] == "v":
        entity = "u" + entity[7:] + "-var-" + entity[3:6]
    return entity.lower()
