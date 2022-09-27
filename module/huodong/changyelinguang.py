from module.huodong.base_huodong import BaseHuoDong


class ChangYeLinGuang(BaseHuoDong):
    def __init__(self, max_fight_time, game, use_medicine=False, medicine_num=0,
                 use_stone=False, stone_num=0):
        super().__init__(max_fight_time, game, use_medicine, medicine_num, use_stone, stone_num)

    @property
    def huodong_name(self):
        return "changyelinguang"

    @property
    def huodong_click(self):
        return 1075, 425, 1173, 451

    @property
    def huodongmain(self):
        return 536, 646, 556, 665, "活"

    @property
    def enter_huodong(self):
        return self.enter_huodong_template["center_one"]


if __name__ == '__main__':
    from module.base import *
    from module.entity.ocr_entity import OcrEntity

    ocr_entity = OcrEntity(x1=536, y1=646, x2=556, y2=665, except_result="活")
    base.ocr(ocr_entity)
    assert ocr_entity.is_except()
