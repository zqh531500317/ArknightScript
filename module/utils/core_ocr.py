import cnocr.utils
from cnocr import CnOcr
from module.utils.core_config import *
from cnstd import CnStd

use = configList["Config"]["Ocr"]["use"]

ocr = CnOcr(model_name="densenet_lite_136-fc")
cnstd = CnStd(rotated_bbox=False, resized_shape=(1280, 704))
ziyuanshouji_tag = "空中威胁资源保障粉碎防御货物运送战术演习固若金汤势不可挡摧枯拉朽身先士卒"
recruit_tag = "医疗干员远程位治新手高级资深近战先锋狙击" \
              "术师卫重装辅助特种支援输出群攻减速生存防护削弱" \
              "移控场爆发召唤快复活费用回机械"
recruit_ocr = CnOcr(model_name="densenet_lite_136-gru", cand_alphabet=recruit_tag)
jijian_ocr = CnOcr(model_name="densenet_lite_136-fc", cand_alphabet=cand_alphabet_officer)
number_ocr = CnOcr(model_name="densenet_lite_136-fc", cand_alphabet="1234567890/")


def ocr_without_position(uri, limit=None, cand_alphabet=None):
    if use == "cnocr":
        res = cnocr_without_position(uri, limit, cand_alphabet)
        logger.info("cnocr result:" + str(res))
        return res
    else:
        pass


def ocr_without_position_low(uri, limit=None):
    if use == "cnocr":
        return cnocr_without_position(uri, limit)
    else:
        pass


def cnocr_without_position(uri, limit, cand_alphabet=None):
    if isinstance(uri, str):
        img = cnocr.utils.read_img(uri)
    else:
        img = uri
    if cand_alphabet is not None and limit is None:
        ocr.set_cand_alphabet(cand_alphabet)
        res = ocr.ocr_for_single_line(img)
        ocr.set_cand_alphabet(None)

    elif limit is None:
        res = ocr.ocr_for_single_line(img)
    else:
        res = limit.ocr_for_single_line(img)
    logger.debug("cnocr :" + str(res))
    return [{'words': "".join(str(i) for i in res[0])}]
