from cjkvi_ids_unicode import __version__
import pytest
import cjkvi_ids_unicode.utils as utils
import cjkvi_ids_unicode.driver as driver
import cjkvi_ids_unicode.constants as constants


@pytest.fixture(scope="session", autouse=True)
def init(request):
    driver.init_raw_data()


def test_version():
    assert __version__ == "0.1.0"


def test_cdp_to_glyphwiki_key():
    assert utils.convert_cdp_to_glyphwiki_key("CDP-i001-86D6") == "cdp-86d6-itaiji-001"
    assert utils.convert_cdp_to_glyphwiki_key("CDP-v001-8851") == "cdp-8851-var-001"


def test_ucs_to_glyphwiki_key():
    assert utils.convert_ucs_to_glyphwiki_key("U-v002+4E11") == "u4e11-var-002"
    assert utils.convert_ucs_to_glyphwiki_key("U-i001+864D") == "u864d-itaiji-001"
    assert utils.convert_ucs_to_glyphwiki_key("U-i001+2D94D") == "u2d94d-itaiji-001"
    assert utils.convert_ucs_to_glyphwiki_key("U+7680") == "u7680"


def test_glyphwiki_resolution():
    glyphwiki = driver.GlyphWiki(constants.GLYPHWIKI_VARIANT_INFO)
    assert glyphwiki.resolve("aj1-02177") == "山"
    assert glyphwiki.resolve("aj1-03708") == "卜"
    assert glyphwiki.resolve("cdp-8cc6") == "亡"
    assert glyphwiki.resolve("cdp-86d6-itaiji-001") == "黽"
    assert glyphwiki.resolve("u2d94d-itaiji-001") == "𭥍"
    assert glyphwiki.resolve("gt-k00880") == "虍"
    assert glyphwiki.resolve("gt-k01770") == "𤰔"
