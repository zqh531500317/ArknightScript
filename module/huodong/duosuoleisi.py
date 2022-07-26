from module.huodong.base_huodong import BaseHuoDong


class DuoSuoLeiSi(BaseHuoDong):
    def __init__(self, max_fight_time, game, use_medicine=False, medicine_num=0,
                 use_stone=False, stone_num=0):
        super().__init__(max_fight_time, game, use_medicine, medicine_num, use_stone, stone_num)

    @property
    def huodong_name(self):
        return "duosuoleisi"

    @property
    def huodong_click(self):
        return 994, 319, 1100, 338

    @property
    def huodongmain(self):
        return 409, 652, 429, 671, "查"
