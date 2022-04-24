import cnocr.utils
from cnocr import CnOcr
from module.utils.core_config import cf, logger
from cnstd import CnStd
from module.entity.ocr_entity import OcrEntity

from module.utils.core_decoratir import singleton

ocr = CnOcr(model_name="densenet_lite_136-fc")
cnstd = CnStd(rotated_bbox=False, resized_shape=(1280, 704))
recruit_ocr = CnOcr(model_name="densenet_lite_136-gru", cand_alphabet=cf.recruit_tag)
jijian_ocr = CnOcr(model_name="densenet_lite_136-fc", cand_alphabet=cf.cand_alphabet_officer)
number_ocr = CnOcr(model_name="densenet_lite_136-fc", cand_alphabet=cf.number_tag)


@singleton
class OcrHandler:
    def __int__(self):
        self.ocr = CnOcr(model_name="densenet_lite_136-fc")

    def ocr(self, ocr_entity: OcrEntity):
        x1 = ocr_entity.x1
        y1 = ocr_entity.y1
        x2 = ocr_entity.x2
        y2 = ocr_entity.y2
        img = ocr_entity.input_img[y1: y2, x1:x2]
        cand_alphabet = ocr_entity.cand_alphabet
        self.ocr.set_cand_alphabet(cand_alphabet)
        temp = self.ocr.ocr_for_single_line(img)
        self.ocr.set_cand_alphabet(None)
        result = [{'words': "".join(str(i) for i in temp[0])}]
        ocr_entity.result = result
        return ocr_entity

    @staticmethod
    def ocr_without_position(uri, limit=None, cand_alphabet=None):
        if cf.get("use") == "cnocr":
            res = cnocr_without_position(uri, limit, cand_alphabet)
            logger.debug("cnocr result:" + str(res))
            return res
        else:
            pass

    @staticmethod
    def ocr_without_position_low(uri, limit=None):
        if cf.get("use") == "cnocr":
            return cnocr_without_position(uri, limit)
        else:
            pass

    @staticmethod
    def cnocr_without_position(uri, limit, cand_alphabet=None):
        if isinstance(uri, str):
            img = cnocr.utils.read_img(uri)
        else:
            img = uri
        if cand_alphabet is not None and limit is None:
            ocr.set_cand_alphabet(cand_alphabet)
            # Returns tuple: (['你', '好'], 0.80)
            res = ocr.ocr_for_single_line(img)
            ocr.set_cand_alphabet(None)

        elif limit is None:
            res = ocr.ocr_for_single_line(img)
        else:
            res = limit.ocr_for_single_line(img)
        logger.debug("cnocr :" + str(res))
        return [{'words': "".join(str(i) for i in res[0])}]


def ocr_without_position(uri, limit=None, cand_alphabet=None):
    if cf.get("use") == "cnocr":
        res = cnocr_without_position(uri, limit, cand_alphabet)
        logger.debug("cnocr result:" + str(res))
        return res
    else:
        pass


def ocr_without_position_low(uri, limit=None):
    if cf.get("use") == "cnocr":
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
        # Returns tuple: (['你', '好'], 0.80)
        res = ocr.ocr_for_single_line(img)
        ocr.set_cand_alphabet(None)

    elif limit is None:
        res = ocr.ocr_for_single_line(img)
    else:
        res = limit.ocr_for_single_line(img)
    logger.debug("cnocr :" + str(res))
    return [{'words': "".join(str(i) for i in res[0])}]


if __name__ == '__main__':
    pass
