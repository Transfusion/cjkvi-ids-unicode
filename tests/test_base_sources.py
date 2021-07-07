from cjkvi_ids_unicode.data_access.ManualEntries import ManualEntries


def test_manual_resolution():
    manual = ManualEntries("tests/test_data/MANUALLY_RESOLVED_IDS-UCS-Ext-E.txt")
    assert manual.get_ids("𬢆") == ["⿱⿰虎↷虎見"]
    assert manual.get_ids("𬴘") == ["⿳亠⿲丨二丨⿳冖⿸丅⿰二丨丅", "⿳亠⿲丨二丨⿳口⿲丨二丨丅"]
