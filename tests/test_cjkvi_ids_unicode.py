from cjkvi_ids_unicode import __version__
import cjkvi_ids_unicode.utils as utils


def test_version():
    assert __version__ == "0.1.0"


def test_cdp_to_glyphwiki_key():
    assert utils.convert_cdp_to_glyphwiki_key("CDP-i001-86D6") == "cdp-86d6-itaiji-001"
    assert utils.convert_cdp_to_glyphwiki_key("CDP-v001-8851") == "cdp-8851-var-001"


def test_ucs_to_glyphwiki_key():
    assert utils.convert_ucs_to_glyphwiki_key("U-v002+4E11") == "u4e11-var-002"
    assert utils.convert_ucs_to_glyphwiki_key("U-i001+864D") == "u864d-itaiji-001"
    assert utils.convert_ucs_to_glyphwiki_key("U-i001+2D94D") == "u2d94d-itaiji-001"