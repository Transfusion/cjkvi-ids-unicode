This directory is for manually added IDS data, also in the format of the source data (CHISE / Kawabata format.) Filenames in this folder are identical to those in `rawdata/ids`. Locale tags (e.g. `U+2CCE7 𬳧 ⿱鄉香[T] ⿱鄕香[M]`) are acceptable.

Each IDS string for each entry in this file will be filtered against `RESOLVED` and `ENTITIES_RESOLVED`. Any remaining strings will make it into `MANUAL_${file name}`.

The purpose of the files in this folder is to manually resolve `UNRESOLVABLE` characters, e.g.　`U+2D27F 𭉿 ⿰口⿱⑧夕` could be expressed as `⿰口⿳丆⺝⿱冖夕` while retaining most of the structural information.

As mentioned in the main README of this project, given the goals of this project, since 目 without the last stroke is not encoded, ⺝ (a variant of 月) is an acceptable substitute.

## Example

Excerpt from `IDS-UCS-Ext-E.txt`:

```
U+2C18B	𬆋	⿰⿱止午⿱止午	⿱𣥖⿰午午
U+2C402	𬐂	⿰⿱癶开士	⿰発士
```

Let's say `IDS-UCS-Ext-E.txt` exists in this folder with the following line:

```
U+2C18B	𬆋	⿰⿱止午⿱止午  ⿱⿰止止⿰午午
```

`MANUAL-UCS-Ext-E.txt` will contain the following line;

```
U+2C18B	𬆋	⿱⿰止止⿰午午
```

since `⿰⿱止午⿱止午` already exists in the original decomposition. The same would apply if `⿰⿱止午⿱止午` was arrived at after entity resolution.
