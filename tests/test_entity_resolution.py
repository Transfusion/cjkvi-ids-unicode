from cjkvi_ids_unicode.data_access.JISX0212 import JISX0212
from cjkvi_ids_unicode.unified_resolver import UnifiedResolver
from cjkvi_ids_unicode.data_access.CNS11643 import CNS11643
from cjkvi_ids_unicode.data_access.HanYouDenShi import HanYouDenShi
from cjkvi_ids_unicode.data_access.MojiJouHouKiban import MojiJouHouKiban
from cjkvi_ids_unicode.data_access.JISX0208 import JISX0208
from cjkvi_ids_unicode.data_access.JISX0213 import JISX0213
from cjkvi_ids_unicode.data_access.GlyphWiki import GlyphWiki

from cjkvi_ids_unicode import __version__, constants

import gzip, shutil, pytest


def test_version():
    assert __version__ == "0.1.0"


@pytest.fixture(scope="session", autouse=True)
def init(request):
    with gzip.open("tests/test_data/dump_newest_only.txt.gz", "rb") as f_in:
        with open("tests/test_data/dump_newest_only.txt", "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)


def test_glyphwiki_resolution():
    glyphwiki = GlyphWiki("tests/test_data/dump_newest_only.txt")
    assert glyphwiki.resolve("aj1-02177") == "山"
    assert glyphwiki.resolve("aj1-03708") == "卜"
    assert glyphwiki.resolve("cdp-8cc6") == "亡"
    assert glyphwiki.resolve("cdp-88a1") == "行"
    assert glyphwiki.resolve("cdp-86d6-itaiji-001") == "黽"
    assert glyphwiki.resolve("u2d94d-itaiji-001") == "𭥍"
    assert glyphwiki.resolve("gt-k00880") == "虍"
    assert glyphwiki.resolve("gt-k01770") == "𤰔"
    assert glyphwiki.resolve("cdp-8c66") == "𧘇"


def test_jisx0208_resolution():
    jisx0208 = JISX0208(constants.JISX0208_INFO)
    assert ord(jisx0208.resolve("376E")) == 26376


def test_jisx0212_resolution():
    jisx0212 = JISX0212(constants.JISX0212_INFO)
    assert ord(jisx0212.resolve("6676")) == 38618


def test_jisx0213_resolution():
    jisx0213 = JISX0213(constants.JISX0213_INFO)
    # 2nd plane, 7E72
    assert ord(jisx0213.resolve(2, "7E72")) == 173594  # 0x2A61A


def test_mojijouhoukiban_resolution():
    mj = MojiJouHouKiban(constants.MOJIJOUHOUKIBAN_INFO)
    assert (
        ord(mj.resolve("MJ000778")) == 14200
    )  # http://ccamc.co/cjkv_mojikiban_radical.php?q=42&rms=7


def test_hanyoudenshi_resolution():
    hd = HanYouDenShi(constants.HANYOUDENSHI_INFO)
    assert ord(hd.resolve("KS502150")) == 169780
    assert ord(hd.resolve("KS278790")) == 31160


def test_cns11643_resolution():
    cns = CNS11643(constants.CNS11643_INFO)
    assert ord(cns.resolve("C4-212F")) == 194600


def test_unified_resolution():
    gw = GlyphWiki("tests/test_data/dump_newest_only.txt")
    jisx0208 = JISX0208(constants.JISX0208_INFO)
    jisx0212 = JISX0212(constants.JISX0212_INFO)
    jisx0213 = JISX0213(constants.JISX0213_INFO)
    mj = MojiJouHouKiban(constants.MOJIJOUHOUKIBAN_INFO)
    hd = HanYouDenShi(constants.HANYOUDENSHI_INFO)
    cns = CNS11643(constants.CNS11643_INFO)

    un = UnifiedResolver(gw, jisx0208, jisx0212, jisx0213, mj, hd, cns)
    assert un.resolve_entity_references("⿹𣦻&A-IWDSU+8C37;") == "⿹𣦻谷"
    assert un.resolve_entity_references("⿰&A-IWDSU+777F;殳") == "⿰睿殳"
    assert un.resolve_entity_references("⿴卯&A-IWDSU+7680;") == "⿴卯皀"

    # test cdp
    assert un.resolve_entity_references("⿰𤣩⿳&CDP-8754;&CDP-v004-8C4F;韭") == "⿰𤣩⿳𦭝癶韭"
    assert un.resolve_entity_references("⿰⿱⿵&CDP-8BC0;巳又頁") == "⿰⿱⿵冂巳又頁"
    assert un.resolve_entity_references("⿱𠙇⿷&CDP-v005-88CB;百") == "⿱𠙇⿷龜百"

    # test cns
    assert un.resolve_entity_references("⿱⿰冫&C3-212D;&C1-4779;") == "⿱⿰冫亇寺"
    assert un.resolve_entity_references("⿰冫&C3-2546;") == "⿰冫夋"

    # test hanyo-denshi
    assert un.resolve_entity_references("⿸⿰&R-HD-JA-376E;龹冫") == "⿸⿰月龹冫"

    assert un.resolve_entity_references("⿱⿱&A-compU+5DDB;龱𠂡") == "⿱⿱巛龱𠂡"
