from cjkvi_ids_unicode.data_access.JISX0212 import JISX0212
from cjkvi_ids_unicode.data_access import (
    CNS11643,
    GlyphWiki,
    HanYouDenShi,
    JISX0208,
    JISX0213,
    MojiJouHouKiban,
)

import cjkvi_ids_unicode.constants as constants
import cjkvi_ids_unicode.utils as utils


class UnifiedResolver:
    def __init__(
        self,
        glyphwiki: GlyphWiki,
        jisx0208: JISX0208,
        jisx0212: JISX0212,
        jisx0213: JISX0213,
        mojijouhou: MojiJouHouKiban,
        hanyoudenshi: HanYouDenShi,
        cns11643: CNS11643,
    ):
        self.glyphwiki = glyphwiki
        self.jisx0208 = jisx0208
        self.jisx0212 = jisx0212
        self.jisx0213 = jisx0213
        self.mojijouhou = mojijouhou
        self.hanyoudenshi = hanyoudenshi
        self.cns11643 = cns11643
        self.entity_map = {}  # for memoization

    def resolve_entity_references(self, ids: str):
        """Input is a complete IDS sequence, output is
        the same sequence but with as many entity references replaced as possible; may be identical to the input if no references were replaced"""
        ampersands = [i for i in range(len(ids)) if ids[i] == "&"]
        semicolons = [i for i in range(len(ids)) if ids[i] == ";"]
        for (begin, end) in zip(ampersands, semicolons):
            res = None
            og_entity = ids[begin + 1 : end]
            entity = og_entity
            if entity in self.entity_map:
                continue

            # strip A-
            if entity.startswith(constants.entity_ref_constants.ALIAS_PREFIX):
                entity = entity[2:]
            # strip R-
            if entity.startswith(constants.entity_ref_constants.R_PREFIX):
                entity = entity[2:]
            if entity.startswith(constants.entity_ref_constants.COMPU_PREFIX):
                res = chr(
                    int(entity[len(constants.entity_ref_constants.COMPU_PREFIX) :], 16)
                )
            if entity.startswith(constants.entity_ref_constants.CDP_PREFIX):
                if len(entity) != 8:  # cdp-xxxx
                    entity = utils.convert_cdp_to_glyphwiki_key(entity)
                res = self.glyphwiki.resolve(entity.lower())
            elif (
                entity.startswith(constants.entity_ref_constants.C1_PREFIX)
                or entity.startswith(constants.entity_ref_constants.C2_PREFIX)
                or entity.startswith(constants.entity_ref_constants.C3_PREFIX)
                or entity.startswith(constants.entity_ref_constants.C4_PREFIX)
                or entity.startswith(constants.entity_ref_constants.C5_PREFIX)
                or entity.startswith(constants.entity_ref_constants.C6_PREFIX)
                or entity.startswith(constants.entity_ref_constants.C7_PREFIX)
            ):
                res = self.cns11643.resolve(entity)
            elif entity.startswith(constants.entity_ref_constants.JX_PREFIX):
                jx_number = int(entity[2])
                res = self.jisx0213.resolve(
                    1 if jx_number == 1 or jx_number == 3 else 2, entity[4:]
                )
            elif entity.startswith(constants.entity_ref_constants.GT_PREFIX):
                res = self.glyphwiki.resolve(entity.lower())
            elif entity.startswith(constants.entity_ref_constants.AJ1_PREFIX):
                res = self.glyphwiki.resolve(entity.lower())
            elif entity.startswith(constants.entity_ref_constants.UCS_PREFIX):
                entity = utils.convert_ucs_to_glyphwiki_key(entity)
                res = self.glyphwiki.resolve(entity)
            elif entity.startswith(constants.entity_ref_constants.HD_PREFIX):
                entity = entity[
                    len(constants.entity_ref_constants.HD_PREFIX) :
                ].replace("-", "")
                subcode = entity[:2]
                if subcode == "JA":
                    res = self.jisx0208.resolve(entity[2:])
                elif subcode == "JB":
                    res = self.jisx0212.resolve(entity[2:])
                # JC and JD unused in UCS
                else:
                    res = self.hanyoudenshi.resolve(entity)
            elif entity.startswith(constants.entity_ref_constants.MJ_PREFIX):
                res = self.mojijouhou.resolve(entity)
            elif entity.startswith(constants.entity_ref_constants.G0_PREFIX):
                res = self.glyphwiki.resolve(entity.lower())
            elif entity.startswith(constants.entity_ref_constants.IWDS_PREFIX):
                entity = entity[len(constants.entity_ref_constants.IWDS_PREFIX) :]
                entity = utils.convert_ucs_to_glyphwiki_key(entity)
                res = self.glyphwiki.resolve(entity)

            if res is None:
                # return None
                pass
            else:
                self.entity_map[og_entity] = res

        # res is not none, replace all of the entities
        full_entity_arr = set(
            [ids[begin : end + 1] for (begin, end) in zip(ampersands, semicolons)]
        )

        for full_entity in full_entity_arr:
            entity = full_entity[1:-1]
            if entity in self.entity_map:
                ids = ids.replace(full_entity, self.entity_map[entity])

        return ids
