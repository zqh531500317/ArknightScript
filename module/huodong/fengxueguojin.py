from module.huodong.base_huodong import BaseHuoDong


class FengXueGuoJin(BaseHuoDong):
    def __init__(self, max_fight_time, game, use_medicine=False, medicine_num=0,
                 use_stone=False, stone_num=0):
        super().__init__(max_fight_time, game, use_medicine, medicine_num, use_stone, stone_num)

    @property
    def huodong_name(self):
        return "fengxueguojin"

    @property
    def huodong_click(self):
        return 1132, 313, 1160, 340

    @property
    def huodongmain(self):
        return 95, 185, 120, 209, "查"
