from cnocr import CnOcr
import cnocr.utils
from cnstd import CnStd

from module.base.config import CoreConfig
from logzero import logger

from module.entity.ocr_entity import OcrEntity


class OcrHandler(CoreConfig):
    def __init__(self):
        super().__init__()
        self.ocr = CnOcr(model_name="densenet_lite_136-fc")
        self.cnstd = CnStd(rotated_bbox=False, resized_shape=(1280, 704))

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

    def ocr_number(self, ocr_entity: OcrEntity):
        x1 = ocr_entity.x1
        y1 = ocr_entity.y1
        x2 = ocr_entity.x2
        y2 = ocr_entity.y2
        img = ocr_entity.input_img[y1: y2, x1:x2]
        cand_alphabet = self.number_tag
        self.ocr.set_cand_alphabet(cand_alphabet)
        temp = self.ocr.ocr_for_single_line(img)
        self.ocr.set_cand_alphabet(None)
        result = [{'words': "".join(str(i) for i in temp[0])}]
        ocr_entity.result = result
        return ocr_entity

    def ocr_jijian(self, ocr_entity: OcrEntity):
        x1 = ocr_entity.x1
        y1 = ocr_entity.y1
        x2 = ocr_entity.x2
        y2 = ocr_entity.y2
        img = ocr_entity.input_img[y1: y2, x1:x2]
        cand_alphabet = self.cand_alphabet_officer
        self.ocr.set_cand_alphabet(cand_alphabet)
        temp = self.ocr.ocr_for_single_line(img)
        self.ocr.set_cand_alphabet(None)
        result = [{'words': "".join(str(i) for i in temp[0])}]
        ocr_entity.result = result
        return ocr_entity

    def ocr_without_position(self, uri, limit=None, cand_alphabet=None):
        if self.get("use") == "cnocr":
            res = self.cnocr_without_position(uri, limit, cand_alphabet)
            logger.debug("cnocr result:" + str(res))
            return res
        else:
            pass

    def ocr_without_position_low(self, uri, limit=None):
        if self.get("use") == "cnocr":
            return self.cnocr_without_position(uri, limit)
        else:
            pass

    def cnocr_without_position(self, uri, limit, cand_alphabet=None):
        if isinstance(uri, str):
            img = cnocr.utils.read_img(uri)
        else:
            img = uri
        if cand_alphabet is not None and limit is None:
            self.ocr.set_cand_alphabet(cand_alphabet)
            # Returns tuple: (['你', '好'], 0.80)
            res = self.ocr.ocr_for_single_line(img)
            self.ocr.set_cand_alphabet(None)

        elif limit is None:
            res = self.ocr.ocr_for_single_line(img)
        else:
            res = limit.ocr_for_single_line(img)
        logger.debug("cnocr :" + str(res))
        return [{'words': "".join(str(i) for i in res[0])}]
