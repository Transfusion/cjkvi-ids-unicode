# Unicode-only IDS data

IDS data in the format of [CHISE](http://www.chise.org/) which avoids, _to the maximum extent possible_, the use of any entity references. 

This dataset is intended for the [Radically](https://github.com/Radically/radically) project, a component-based CJK character search engine which currently only handles UCS/UTF-8 characters; being able to look up characters with the semantic equivalents of their subcomponents, even if not structurally exact, is extremely useful.

Examples of IDSes containing entity references which have exact semanto-structural Unicode counterparts:

```
U+877E 蝾 ⿱虫&AJ1-17775; (荣)
U+8C50 豐 ⿱&CDP-8D51;豆 (𠁳)
U+4049 䁉 ⿱&hanaJU+2BF09;目 (𫼉)
U+FA1F 﨟 ⿱艹&M-29726; (𦝲)
U-00027F3C 𧼼 ⿺走&GT-40124; (若)
```
## Substitution heuristics
A list of entity reference formats may be found in these papers: [Multiple-policy Character Annotation based on CHISE](https://www.jstage.jst.go.jp/article/jjadh/1/1/1_86/_pdf), pg. 16 and [Possibilities of integration between a glyph-image database for Kanji
characters and a character ontology](https://ipsj.ixsq.nii.ac.jp/ej/index.php?action=pages_view_main&active_action=repository_action_common_download&item_id=82411&item_no=1&attribute_id=1&file_no=1&page_id=13&block_id=8), pg. 5.

The current entity prefixes being handled are (with examples):

- &**A**-IWDSU+777F; (A-, alias prefix, strip and attempt to resolve the remainder of the string)
- &**R**-HD-JA-376E; (R-, ??, strip and attempt to resolve the remainder of the string)
- &A-**compU**+5DDB; (compU+, ?? strip and convert to UCS/UTF-8 character)
- &CDP-8C66; (CDP-, Chinese Document Processing lab's internal code for various components in 「[漢字構形資料庫](https://cdp.sinica.edu.tw/cdphanzi/code.htm)」. Resolve to the nearest 関連字 using GlyphWiki's dump.)
- &**U**-i003+51AC; (U-, variants of Unicode characters; strip all the variant information and convert to UCS/UTF-8 character)
- &**C4**-212F; (C[1-7]-, CNS11643 charset characters, resolve with the tables found in [https://gitlab.chise.org/CHISE/xemacs-chise](xemacs-chise)
- &**GT-K**01770; (GT- or GT-K, a font with a large collection of CJK chars and their variants. Resolve to the nearest 関連字 using GlyphWiki's dump.) More information:
    - https://glyphwiki.org/wiki/Group:GT%e3%82%b3%e3%83%bc%e3%83%89
    - http://web.archive.org/web/20190714090304/http://charcenter.tron.org/tfont/about_gt.html
- &R-**HD-JA**-376E; (HD-, organized by the 汎用電子情報交換環境整備プログラム . Sub-prefixes usually correspond to well-known charsets; HD-JA corresponds to JIS X0208, HD-JD JIS X0213 plane 1, HD-KS 戸籍統一文字, etc. Resolve using lookup tables.)
- &**JX**2-793E; (JX[1-3]-, corresponds to various versions of the JIS charset. Refer to the papers above. Resolve using lookup tables.)
- &**MJ**000778; (MJ, 「文字情報基盤」codepoints. Lookup tables are available on the [moji.or.jp](https://moji.or.jp/mojikiban/mjlist/) website.)
- &**G0**-4056; (G0-, ??? Resolve to the nearest 関連字 using GlyphWiki's dump.)


`cjkvi_ids_unicode.data_access.EntityResolver` is subclassed for each of these sources, and fed into `cjkvi_ids_unicode.unified_resolver.resolve_entity_references`.


## Notes on GlyphWiki resolution
An algorithm determining the nearest 関連字 using GlyphWiki's `dump_newest_only.txt` may be found in `cjkvi_ids_unicode.data_access.GlyphWiki`. It is invented my me and is known to be incorrect in certain cases.

Essentially, it recursively searches the `related` column until `u3013` is reached (`u3013` being the [placeholder character](https://glyphwiki.org/wiki/GlyphWiki:%E9%AB%98%E5%BA%A6%E3%81%AA%E6%B4%BB%E7%94%A8%E6%96%B9%E6%B3%95)), and then checks if it the glyph begins with the signature KAGE engine bounding box, `99:0:0:0:0:200:200`, which indicates that it is fully defined in terms of another glyph. 

The logic is that non-suffixed UCS characters, e.g. `u2667e`, should be aliased to hyphenated characters such as `u2667e-j`; Simplified Chinese characters are thus aliased to `-g`. This falls apart due to data inconsistency and not all 表外 characters being related to a UCS character.

## Licenses

`SPDX-License-Identifier: MIT OR GPL-2.0-or-later`

- The products of this repository (`*IDS*.txt` and `*IDS*.json`) are licensed under the GNU General Public License v2.0 or later.
    - They are derived from CHISE and the [Kanji Database Project](http://kanji-database.sourceforge.net/index.html), which use the GPLv2.
- The code written by me is dual-licensed under the GNU General Public License v2.0 or later, and the MIT license.
    - If you adapt and use it for its evident intended purpose (fetching and processing IDSs from CHISE and the Kanji Database Project), you must release your changes under the GPLv2+.
    - I do not see how it is very useful for anything other than its evident intended purpose, but if, say, you take the lookup table logic and the HTML generation logic on their own stackoverflow-style with no relation to the aforementioned sources, you may use such snippets under the MIT license. I'd still like to know how you find it useful, in such cases.
