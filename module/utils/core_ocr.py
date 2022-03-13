import cnocr.utils
from aip import AipOcr
from cnocr import CnOcr
from .core_config import *
from cnstd import CnStd

use = configList["Config"]["Ocr"]["use"]

APP_ID = configList["Config"]["Ocr"]["baidu"]["APP_ID"]
API_KEY = configList["Config"]["Ocr"]["baidu"]["API_KEY"]
SECRET_KEY = configList["Config"]["Ocr"]["baidu"]["SECRET_KEY"]
ocr = CnOcr(model_name="densenet_lite_136-fc")
cnstd = CnStd(rotated_bbox=False, resized_shape=(1280, 704))
recruit_tag = "医疗干员远程位治新手高级资深近战先锋狙击" \
              "术师卫重装辅助特种支援输出群攻减速生存防护削弱" \
              "移控场爆发召唤快复活费用回机械"
recruit_ocr = CnOcr(model_name="densenet_lite_136-gru", cand_alphabet=recruit_tag)
jijian_ocr = CnOcr(model_name="densenet_lite_136-fc", cand_alphabet=cand_alphabet_officer)
number_ocr = CnOcr(model_name="densenet_lite_136-fc", cand_alphabet="1234567890/")


def ocr_with_position(uri, limit=None):
    if use == "baidu":
        res = baiduOCR_with_position(uri)
        logger.info("baidu ocr result:" + str(res))
        return res
    elif use == "cnocr":
        res = baiduOCR_with_position(uri)
        logger.info("baidu result:" + str(res))
        return res
    else:
        pass


def ocr_without_position(uri, limit=None):
    if use == "baidu":
        res = baiduOCR_without_position(uri)
        logger.info("baidu ocr result:" + str(res))
        return res
    elif use == "cnocr":
        res = cnocr_without_position(uri, limit)
        logger.info("cnocr result:" + str(res))
        return res
    else:
        pass


def ocr_without_position_low(uri, limit=None):
    if use == "baidu":
        return baiduOCR_without_position_low(uri)
    elif use == "cnocr":
        return cnocr_without_position(uri, limit)
    else:
        pass


def cnocr_without_position(uri, limit):
    img = cnocr.utils.read_img(uri)
    if limit is None:
        res = ocr.ocr_for_single_line(img)
    else:
        res = limit.ocr_for_single_line(img)
    logger.debug("cnocr :" + str(res))
    return [{'words': "".join(str(i) for i in res[0])}]


def baiduOCR_with_position(uri):
    # 百度提供
    """ 你的 APPID AK SK """
    a = str(APP_ID)  # 应用的appid
    b = API_KEY  # 应用的appkey
    c = SECRET_KEY  # 应用的secretkey
    client = AipOcr(a, b, c)
    i = open(uri, 'rb')
    img = i.read()
    message = client.general(img)
    i.close()
    return message.get('words_result')


def baiduOCR_without_position(uri):
    # 百度提供
    """ 你的 APPID AK SK """
    a = str(APP_ID)  # 应用的appid
    b = API_KEY  # 应用的appkey
    c = SECRET_KEY  # 应用的secretkey
    client = AipOcr(a, b, c)
    i = open(uri, 'rb')
    img = i.read()
    message = client.basicAccurate(img)
    i.close()
    return message.get('words_result')


def baiduOCR_without_position_low(uri):
    # 百度提供
    """ 你的 APPID AK SK """
    a = str(APP_ID)  # 应用的appid
    b = API_KEY  # 应用的appkey
    c = SECRET_KEY  # 应用的secretkey
    client = AipOcr(a, b, c)
    i = open(uri, 'rb')
    img = i.read()
    message = client.basicGeneralUrl(img)
    i.close()
    return message.get('words_result')
