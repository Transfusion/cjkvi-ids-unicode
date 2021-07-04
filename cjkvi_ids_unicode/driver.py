from cjkvi_ids_unicode.metadata_generator import MetadataGenerator
from collections import defaultdict
from cjkvi_ids_unicode.data_access.Chise import Chise
from cjkvi_ids_unicode.data_access.Kawabata import Kawabata

from cjkvi_ids_unicode.data_access.JISX0212 import JISX0212
from cjkvi_ids_unicode.unified_resolver import UnifiedResolver
from cjkvi_ids_unicode.data_access.CNS11643 import CNS11643
from cjkvi_ids_unicode.data_access.HanYouDenShi import HanYouDenShi
from cjkvi_ids_unicode.data_access.MojiJouHouKiban import MojiJouHouKiban
from cjkvi_ids_unicode.data_access.JISX0208 import JISX0208
from cjkvi_ids_unicode.data_access.JISX0213 import JISX0213
from cjkvi_ids_unicode.data_access.GlyphWiki import GlyphWiki

from cjkvi_ids_unicode.data_access.ManualEntries import ManualEntries

import cjkvi_ids_unicode.constants as constants
import cjkvi_ids_unicode.utils as utils
from cjkvi_ids_unicode.types import CharIDSTuple, IDSDict
import typing
from pathlib import Path
from tqdm import tqdm
from shutil import copyfile
import sys, os, glob, csv, tarfile, requests, datetime, json


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

    # replaced by MJ文字情報一覧表
    # if not os.path.exists(constants.MOJIJOUHOUKIBAN_INFO):
    #     folder = constants.MOJIJOUHOUKIBAN_ROOT_FOLDER
    #     if not os.path.exists(folder):
    #         os.mkdir(folder)
    #     # download and extract
    #     download_file(
    #         "http://mojikiban.ipa.go.jp/mjc/IVD_Sequences.txt",
    #         constants.MOJIJOUHOUKIBAN_INFO,
    #     )

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


def write_char_ids_to_file(ls: list[CharIDSTuple], filepath):
    with open(
        filepath,
        "w",
    ) as _file:
        for (char, ids) in ls:
            cp = f"U+{ord(char):x}".upper()
            ids = "\t".join(ids)
            _file.write(f"{cp}\t{char}\t{ids}\n")
        _file.close()


class EntityReplacementTracker:
    """
    Encapsulates characters and their IDSes containing entity strings -> IDSes with at least 1 of said strings replaced
    """

    def __init__(self):
        self.m: typing.DefaultDict[str, list[list[str]]] = defaultdict(list)

    def add_entry(self, char: str, pair: list[str]):
        """
        pair is a list containing only 2 elements, the 1st being the original IDS and the 2nd being the (partially) resolved IDS
        """
        self.m[char].append(pair)

    def write_to_json_file(self, original_file_name: str):
        original_file_name = os.path.splitext(original_file_name)[0]
        with open(
            os.path.join(
                constants.OUTPUT_DIR,
                constants.ENTITIES_REPLACED_FILE_NAME_TEMPLATE.format(
                    original_file_name
                ),
            ),
            "w",
        ) as outfile:
            json.dump(self.m, outfile, indent=2, ensure_ascii=False)


def write_no_full_resolution_map_to_file(m: IDSDict, original_file_name: str):
    for key in m.keys():
        m[key] = list(set(m[key]))
    original_file_name = os.path.splitext(original_file_name)[0]
    with open(
        os.path.join(
            constants.OUTPUT_DIR,
            constants.NO_FULL_RESOLUTION_FILE_NAME_TEMPLATE.format(original_file_name),
        ),
        "w",
    ) as outfile:
        json.dump(m, outfile, indent=2, ensure_ascii=False)


def cli(args=None):
    create_output_dir()
    init_raw_data()
    glyphwiki = GlyphWiki(constants.GLYPHWIKI_VARIANT_INFO)
    jisx0208 = JISX0208(constants.JISX0208_INFO)
    jisx0212 = JISX0212(constants.JISX0212_INFO)
    jisx0213 = JISX0213(constants.JISX0213_INFO)
    mj = MojiJouHouKiban(constants.MOJIJOUHOUKIBAN_INFO)
    hd = HanYouDenShi(constants.HANYOUDENSHI_INFO)
    cns = CNS11643(constants.CNS11643_INFO)

    resolver = UnifiedResolver(glyphwiki, jisx0208, jisx0212, jisx0213, mj, hd, cns)

    kawabata_ab = Kawabata(constants.KAWABATA_IDS_AB)
    kawabata_cdef = Kawabata(constants.KAWABATA_IDS_CDEF)

    metadata_generator = MetadataGenerator()
    for f in os.listdir(constants.CHISE_IDS_ROOT_FOLDER):
        tracker = EntityReplacementTracker()
        resolved: list[CharIDSTuple] = []  # list of tuple of char, [ids]
        partially_resolved: list[CharIDSTuple] = []

        resolved_map: typing.DefaultDict[str, list[str]] = defaultdict(list)
        partially_resolved_map: typing.DefaultDict[str, list[str]] = defaultdict(list)

        no_full_resolution_map: IDSDict = (
            {}
        )  # chars which are only present in partially_resolved_map but not in resolved_map

        if not f.startswith(constants.CHISE_IDS_UCS_PREFIX):
            continue
        manual_ids: ManualEntries = ManualEntries(
            os.path.join(constants.MANUAL_IDS_ROOT_FOLDER, f)
        )

        manual_ids_partial = ManualEntries(
            os.path.join(constants.MANUAL_IDS_ROOT_FOLDER, "PARTIAL_" + f)
        )

        chise: Chise = Chise(os.path.join(constants.CHISE_IDS_ROOT_FOLDER, f))
        # copy this file into the output for gh-pages
        copyfile(
            os.path.join(constants.CHISE_IDS_ROOT_FOLDER, f),
            os.path.join(constants.OUTPUT_DIR, constants.ORIGINAL_FILE_PREFIX + f),
        )

        for char in chise.map:
            kawabata: Kawabata = None
            if char in kawabata_ab.map:
                kawabata = kawabata_ab
            elif char in kawabata_cdef.map:
                kawabata = kawabata_cdef

            if kawabata:
                for ids in kawabata.get_all_ids(char):
                    if utils.is_valid_ids(ids):
                        resolved_map[char].append(ids)
                    elif ids != "?":
                        partially_resolved_map[char].append(ids)

            for ids in chise.get_all_ids(char):
                if utils.is_valid_ids(ids):
                    resolved_map[char].append(ids)
                elif ids != "?":
                    partially_resolved_map[char].append(ids)

            for ids in manual_ids.get_ids(char):
                if utils.is_valid_ids(ids):
                    resolved_map[char].append(ids)

            for ids in manual_ids_partial.get_ids(char):
                partially_resolved_map[char].append(ids)

        to_del = []
        # attempt to resolve all of the partially resolved entries
        for char in partially_resolved_map.keys():
            new_partially_resolved: list[str] = []
            for ids in partially_resolved_map[char]:
                res = resolver.resolve_entity_references(ids)
                if utils.is_valid_ids(res):
                    resolved_map[char].append(res)
                else:
                    new_partially_resolved.append(res)

                # add to entity replacement debugging output
                if res != ids:
                    tracker.add_entry(char, [ids, res])

            if not new_partially_resolved:
                to_del.append(char)
            else:
                partially_resolved_map[char] = new_partially_resolved

        for char in to_del:
            del partially_resolved_map[char]

        # write to output
        for char in resolved_map:
            resolved.append((char, list(set(resolved_map[char]))))
        for char in partially_resolved_map:
            partially_resolved.append((char, list(set(partially_resolved_map[char]))))

        write_char_ids_to_file(
            resolved,
            os.path.join(constants.OUTPUT_DIR, constants.RESOLVED_FILE_PREFIX + f),
        )

        # write partially resolved to file
        write_char_ids_to_file(
            partially_resolved,
            os.path.join(
                constants.OUTPUT_DIR, constants.PARTIALLY_RESOLVED_FILE_PREFIX + f
            ),
        )
        tracker.write_to_json_file(f)
        for char in partially_resolved_map:
            if char not in resolved_map:
                no_full_resolution_map[char] = partially_resolved_map[char]

        write_no_full_resolution_map_to_file(no_full_resolution_map, f)

        metadata_generator.add_ids_data(
            f, chise.map.keys(), resolved, partially_resolved, no_full_resolution_map
        )
    metadata_generator.generate_html()