import typing
from pathlib import Path
from tqdm import tqdm
import sys, os, glob, csv, tarfile, requests, datetime
import cjkvi_ids_unicode.constants as constants
import cjkvi_ids_unicode.utils as utils

STROKE_PLACEHOLDERS = set(
    [
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

ENTITY_PREFIXES = []


def ids_contains_stroke_placeholders(ids: str):
    """Such an IDS is incomplete and unresolvable. Example: 𭖲⿳⑦人山"""
    return set(ids).intersection(STROKE_PLACEHOLDERS)


def is_valid_ids(ids: str):
    return ("&" not in ids) and not ids_contains_stroke_placeholders(ids)


class Kawabata:
    def __init__(self, input_file_path):
        self.input_file_path = input_file_path
        self.map = {}
        t = open(self.input_file_path)
        while True:
            line = t.readline()
            if line.startswith(";") or line.startswith("#"):
                continue
            if not line:
                break

            split = list(map(lambda x: x.strip(), line.split("\t")))
            char, ids = chr(int(split[0][2:], 16)), split[2:]
            self.map[char] = ids
        t.close()

    def get_valid_ids(self, char):
        if char not in self.map:
            return []
        else:
            return list(filter(lambda x: is_valid_ids(x), self.map[char]))


class Chise:
    def __init__(self, input_file_path):
        self.input_file_path = input_file_path
        self.map = {}
        t = open(self.input_file_path)
        while True:
            line = t.readline()
            if line.startswith(";"):
                continue
            if not line:
                break

            split = list(map(lambda x: x.strip(), line.split("\t")))
            char, ids = chr(int(split[0][2:], 16)), split[2:]
            self.map[char] = ids
        t.close()

    def get_valid_ids(self, char):
        if char not in self.map:
            return []
        else:
            return list(filter(lambda x: is_valid_ids(x), self.map[char]))


# TODO: this class should be relatively testable


class GlyphWiki:
    KAGE_FULL_BOUNDING_BOX = "99:0:0:0:0:200:200:"

    class Entry:
        def __init__(self, related, data):
            self.related = related
            self.data = data

        def __repr__(self):
            return f"<{self.related} {self.data}>"

    def __init__(self, input_file_path):
        self.input_file_path = input_file_path
        self.map = {}
        t = open(self.input_file_path)
        while True:
            line = t.readline()
            if (
                line.startswith("     ")
                or line.startswith("-")
                or line.startswith(" abc")
                or line.startswith("(")
            ):
                continue
            if not line:
                break
            entry = map(lambda x: x.strip(), line.split("|"))
            entry = list(entry)
            if len(entry) < 3:
                continue
            self.map[entry[0]] = GlyphWiki.Entry(entry[1], entry[2])
        t.close()

    def resolve(self, entity_reference: str):
        base_entity_reference = entity_reference
        try:
            base_entity_reference = entity_reference[: entity_reference.index("-")]
        except ValueError:
            pass

        if entity_reference not in self.map:
            return None
        entry = self.map[entity_reference]
        if entry.related == "u3013":
            if entry.data.startswith(GlyphWiki.KAGE_FULL_BOUNDING_BOX):
                alias = entry.data[len(GlyphWiki.KAGE_FULL_BOUNDING_BOX) :]
                return self.resolve(alias)
            else:
                return None

        # there is an infinite loop between u5c71-j and u5c71 lol
        elif (
            entry.related == entity_reference or entry.related == base_entity_reference
        ):
            return chr(int(entry.related[1:], 16))
        else:
            return self.resolve(entry.related)


class JISX0213:
    def __init__(self, input_file_path):
        self.input_file_path = input_file_path
        self.map = {}
        t = open(self.input_file_path)
        while True:
            line = t.readline()
            if line.startswith("#"):
                continue
            if not line:
                break
            entry = line.split("\t")
            self.map[entry[0]] = entry[1]
        t.close()

    def resolve(self, plane: int, code: str):
        return self.map.get(f"{plane+1}-{code.upper()}", None)


# class DaiKanWa:
#     def __init__(self, input_file_path):
#         self.input_file_path = input_file_path
#         self.map = {}
#         t = open(self.input_file_path)
#         while True:
#             line = t.readline()
#             if line.startswith("#"):
#                 continue
#             if not line:
#                 break
#             if not line[0].isdigit():
#                 continue

#             entry = line.split("\t")
#             print(entry)
#             self.map[entry[0]] = chr(int(entry[1][2:].strip(), 16))

#         t.close()


class MojiJouHouKiban:
    def __init__(self, input_file_path):
        self.input_file_path = input_file_path
        self.map = {}
        t = open(self.input_file_path)
        while True:
            line = t.readline()
            if line.startswith("#"):
                continue
            if not line:
                break
            entry = line.split(" ")
            self.map[entry[-1].strip()] = chr(int(entry[0], 16))
        t.close()


class HanYouDenShi:
    def __init__(self, input_file_path):
        self.input_file_path = input_file_path
        self.map = {}
        t = open(self.input_file_path)
        while True:
            line = t.readline()
            if line.startswith("#"):
                continue
            if not line:
                break
            entry = line.split(" ")
            self.map[entry[-1].strip()] = chr(int(entry[0], 16))
        t.close()

    def resolve(self, entity_reference: str):
        return self.map.get(entity_reference, None)


class CNS11643:
    def __init__(self, cns11643_file_paths):
        self.input_file_paths = cns11643_file_paths
        self.map = {}
        for plane in cns11643_file_paths:
            t = open(cns11643_file_paths[plane])
            while True:
                line = t.readline()
                if line.startswith("#"):
                    continue
                if not line:
                    break
                entry = line.split("\t")
                try:
                    self.map[entry[0]] = chr(int(entry[1].strip()[2:], 16))
                except Exception:
                    pass
            t.close()

    def resolve(self, entity_reference: str):
        return self.map.get(entity_reference, None)


def create_output_dir():
    if not os.path.exists(constants.OUTPUT_DIR):
        os.makedirs(constants.OUTPUT_DIR)
    else:
        # delete all files
        files = glob.glob(constants.OUTPUT_DIR + "/*")
        for f in files:
            os.remove(f)


def download_file(url, file):
    # file = url.split("/")[-1]
    r = requests.get(url, stream=True, allow_redirects=True)
    total_size = int(r.headers.get("content-length"))
    initial_pos = 0
    with open(file, "wb") as f:
        with tqdm(
            total=total_size,
            unit="B",
            unit_scale=True,
            desc=file,
            initial=initial_pos,
            ascii=True,
        ) as pbar:
            for ch in r.iter_content(chunk_size=1024):
                if ch:
                    f.write(ch)
                    pbar.update(len(ch))
            f.close()


def init_raw_data():
    # check whether it exists
    if not os.path.exists(constants.GLYPHWIKI_VARIANT_INFO):
        folder = os.path.split(constants.GLYPHWIKI_VARIANT_INFO)[0]
        if not os.path.exists(folder):
            os.mkdir(folder)
        # download and extract
        cur_day = datetime.datetime.now().strftime("%d")
        glyphwiki_file = os.path.join(constants.GLYPHWIKI_ROOT_FOLDER, "dump.tar.gz")
        download_file(
            f"http://kage.osdn.jp/glyphwiki/dump{cur_day}.tar.gz",
            glyphwiki_file,
        )
        tar = tarfile.open(glyphwiki_file, "r:gz")
        tar.extract(
            constants.GLYPHWIKI_NEWEST_DUMP_NAME, path=constants.GLYPHWIKI_ROOT_FOLDER
        )
        tar.close()

    if not os.path.exists(constants.MOJIJOUHOUKIBAN_INFO):
        folder = constants.MOJIJOUHOUKIBAN_ROOT_FOLDER
        if not os.path.exists(folder):
            os.mkdir(folder)
        # download and extract
        download_file(
            "http://mojikiban.ipa.go.jp/mjc/IVD_Sequences.txt",
            constants.MOJIJOUHOUKIBAN_INFO,
        )

    # DaiKanWa can be looked up through the GlyphWiki dump.

    # if not os.path.exists(constants.DAIKANWA_UCS_INFO):
    #     folder = constants.DAIKANWA_ROOT_FOLDER
    #     if not os.path.exists(folder):
    #         os.mkdir(folder)
    #     # download and extract
    #     download_file(
    #         "http://mojikiban.ipa.go.jp/lab/xb3428/daikanwa-ucs.txt",
    #         constants.DAIKANWA_UCS_INFO,
    #     )


def cli(args=None):
    # create_output_dir()
    init_raw_data()
    glyphwiki = GlyphWiki(constants.GLYPHWIKI_VARIANT_INFO)
    kawabata_ab = Kawabata(constants.KAWABATA_IDS_AB)
    kawabata_cdef = Kawabata(constants.KAWABATA_IDS_CDEF)
    jisx0213 = JISX0213(constants.JISX0213_INFO)
    mojijouhou = MojiJouHouKiban(constants.MOJIJOUHOUKIBAN_INFO)
    # daikanwa = DaiKanWa(constants.DAIKANWA_UCS_INFO)
    hanyoudenshi = HanYouDenShi(constants.HANYOUDENSHI_INFO)
    cns11643 = CNS11643(constants.CNS11643_INFO)
    # return

    entity_map = {}

    def resolve_entity_references(ids: str):
        print("resolving entity references", ids)
        """Input is a complete IDS sequence, output is
        the same sequence but with all entity references replaced or None"""
        ampersands = [i for i in range(len(ids)) if ids[i] == "&"]
        semicolons = [i for i in range(len(ids)) if ids[i] == ";"]
        for (begin, end) in zip(ampersands, semicolons):
            res = None
            og_entity = ids[begin + 1 : end]
            entity = og_entity
            if entity in entity_map:
                continue

            # strip A-
            if entity.startswith(constants.entity_ref_constants.ALIAS_PREFIX):
                entity = entity[2:]
            print(entity)
            if entity.startswith(constants.entity_ref_constants.CDP_PREFIX):
                if len(entity) != 8:  # cdp-xxxx
                    entity = utils.convert_cdp_to_glyphwiki_key(entity)
                res = glyphwiki.resolve(entity.lower())
            elif (
                entity.startswith(constants.entity_ref_constants.C1_PREFIX)
                or entity.startswith(constants.entity_ref_constants.C2_PREFIX)
                or entity.startswith(constants.entity_ref_constants.C3_PREFIX)
                or entity.startswith(constants.entity_ref_constants.C4_PREFIX)
                or entity.startswith(constants.entity_ref_constants.C5_PREFIX)
                or entity.startswith(constants.entity_ref_constants.C6_PREFIX)
                or entity.startswith(constants.entity_ref_constants.C7_PREFIX)
            ):
                res = cns11643.resolve(entity)
            elif entity.startswith(constants.entity_ref_constants.JX_PREFIX):
                jx_number = int(entity[2])
                res = jisx0213.resolve(
                    1 if jx_number == 1 or jx_number == 3 else 2, entity[4:]
                )
            elif entity.startswith(constants.entity_ref_constants.GT_PREFIX):
                res = glyphwiki.resolve(entity.lower())
            elif entity.startswith(constants.entity_ref_constants.AJ1_PREFIX):
                res = glyphwiki.resolve(entity.lower())
            elif entity.startswith(constants.entity_ref_constants.UCS_PREFIX):
                print("resolving via gw")
                entity = utils.convert_ucs_to_glyphwiki_key(entity)
                res = glyphwiki.resolve(entity)
                print("gw resolution obtained")
                print(res)
            elif entity.startswith(constants.entity_ref_constants.HD_PREFIX):
                entity = entity[
                    len(constants.entity_ref_constants.HD_PREFIX) :
                ].replace("-", "")
                res = hanyoudenshi.resolve(entity)

            if res is None:
                # return None
                pass
            else:
                entity_map[og_entity] = res

        # res is not none, replace all of the entities
        full_entity_arr = set(
            [ids[begin : end + 1] for (begin, end) in zip(ampersands, semicolons)]
        )

        for full_entity in full_entity_arr:
            entity = full_entity[1:-1]
            if entity in entity_map:
                ids = ids.replace(full_entity, entity_map[entity])

        return ids

    # print(kawabata_ab.map)
    for f in os.listdir(constants.CHISE_IDS_ROOT_FOLDER):
        resolved = []  # list of tuple of char, [ids]
        unresolved = []  # list of tuple of char, [ids] (ids from CHISE)
        entities_resolved = (
            []
        )  # list of tuple of char, [ids] (lost structural information)
        unresolvable = []  # list of tuple of char, [ids]
        partially_resolved = []

        if f.startswith(constants.CHISE_IDS_UCS_PREFIX):
            chise = Chise(os.path.join(constants.CHISE_IDS_ROOT_FOLDER, f))

            for char in chise.map:
                kawabata = None
                if char in kawabata_ab.map:
                    kawabata = kawabata_ab
                elif char in kawabata_cdef.map:
                    kawabata = kawabata_cdef

                if kawabata is None:
                    chise_ids = chise.get_valid_ids(char)
                    if len(chise_ids):
                        resolved.append((char, chise_ids))
                    else:
                        unresolved.append((char, chise.map[char]))
                    continue

                kb_ids = kawabata.get_valid_ids(char)
                chise_ids = chise.get_valid_ids(char)

                if len(kb_ids):
                    resolved.append((char, kb_ids))
                elif len(chise_ids):
                    resolved.append((char, chise_ids))
                else:
                    unresolved.append((char, chise.map[char]))

            # write resolved to file
            with open(
                os.path.join(constants.OUTPUT_DIR, constants.RESOLVED_FILE_PREFIX + f),
                "w",
            ) as _file:
                for (char, ids) in resolved:
                    cp = f"U+{ord(char):x}".upper()
                    ids = "\t".join(ids)
                    _file.write(f"{cp}\t{char}\t{ids}\n")
                _file.close()

            # write unresolved to file
            with open(
                os.path.join(
                    constants.OUTPUT_DIR, constants.UNRESOLVED_FILE_PREFIX + f
                ),
                "w",
            ) as _file:
                for (char, ids) in unresolved:
                    cp = f"U+{ord(char):x}".upper()
                    ids = "\t".join(ids)
                    _file.write(f"{cp}\t{char}\t{ids}\n")
                _file.close()

            # resolve all the unresolved using rawdata
            for (char, ids_arr) in unresolved:
                res_ids_arr = []
                is_unresolvable = False
                for ids in ids_arr:
                    resolved_ids_string = resolve_entity_references(ids)
                    if not is_valid_ids(resolved_ids_string):
                        is_unresolvable = True
                        if resolved_ids_string != ids:
                            res_ids_arr.append(resolved_ids_string)

                if is_unresolvable:
                    if len(res_ids_arr):
                        partially_resolved.append((char, res_ids_arr))
                    else:
                        unresolvable.append((char, ids_arr))
                else:
                    entities_resolved.append((char, res_ids_arr))

            # write entities resolved to file
            with open(
                os.path.join(
                    constants.OUTPUT_DIR, constants.ENTITIES_RESOLVED_FILE_PREFIX + f
                ),
                "w",
            ) as _file:
                for (char, ids) in entities_resolved:
                    cp = f"U+{ord(char):x}".upper()
                    ids = "\t".join(ids)
                    _file.write(f"{cp}\t{char}\t{ids}\n")
                _file.close()

            # write unresolvable to file
            with open(
                os.path.join(
                    constants.OUTPUT_DIR, constants.UNRESOLVABLE_FILE_PREFIX + f
                ),
                "w",
            ) as _file:
                for (char, ids) in unresolvable:
                    cp = f"U+{ord(char):x}".upper()
                    ids = "\t".join(ids)
                    _file.write(f"{cp}\t{char}\t{ids}\n")
                _file.close()

            # write partially resolved to file
            with open(
                os.path.join(
                    constants.OUTPUT_DIR,
                    constants.ENTITIES_PARTIALLY_RESOLVED_FILE_PREFIX + f,
                ),
                "w",
            ) as _file:
                for (char, ids) in partially_resolved:
                    cp = f"U+{ord(char):x}".upper()
                    ids = "\t".join(ids)
                    _file.write(f"{cp}\t{char}\t{ids}\n")
                _file.close()
            break
