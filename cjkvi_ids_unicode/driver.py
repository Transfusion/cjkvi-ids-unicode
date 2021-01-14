import typing
from pathlib import Path
from tqdm import tqdm
import sys, os, glob, csv, tarfile, requests, datetime
import cjkvi_ids_unicode.constants as constants

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


def is_valid_ids(ids: str):
    return ("&" not in ids) and (not set(ids).intersection(STROKE_PLACEHOLDERS))


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

    def get_valid_ids(self, char):
        if char not in self.map:
            return []
        else:
            return list(filter(lambda x: is_valid_ids(x), self.map[char]))


class GlyphWiki:
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
            entry = map(lambda x: x.strip().upper(), line.split("|"))
            entry = list(entry)
            if len(entry) < 3:
                continue
            self.map[entry[0]] = GlyphWiki.Entry(entry[1], entry[2])


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


def cli(args=None):
    create_output_dir()
    init_raw_data()
    glyphwiki = GlyphWiki(constants.GLYPHWIKI_VARIANT_INFO)
    kawabata_ab = Kawabata(constants.KAWABATA_IDS_AB)
    kawabata_cdef = Kawabata(constants.KAWABATA_IDS_CDEF)

    def resolve_entity_references(ids):
        """Input is a complete IDS sequence, output is
        the same sequence but with all entity references replaced."""
        ampersands = [i for i in range(len(ids)) if ids[i] == "&"]
        semicolons = [i for i in range(len(ids)) if ids[i] == ";"]
        for begin, end in zip(ampersands, semicolons):
            entity = ids[begin + 1, end]
        pass

    # print(kawabata_ab.map)
    for f in os.listdir(constants.CHISE_IDS_ROOT_FOLDER):
        resolved = []  # list of tuple of char, [ids]
        unresolved = []  # list of tuple of char, [ids] (ids from CHISE)
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

            # resolve all the unresolved using glyphwiki

            break
