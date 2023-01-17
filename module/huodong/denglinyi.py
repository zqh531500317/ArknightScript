from module.huodong.base_huodong import BaseHuoDong


class DengLinYi(BaseHuoDong):
    @property
    def huodong_name(self):
        return "denglinyi"

    @property
    def huodong_click(self):
        return 1147, 655, 1190, 668

    @property
    def huodongmain(self):
        return 34, 533, 51, 549, "作"

    @property
    def enter_huodong(self):
        return self.enter_huodong_template["left"]

    def __init__(self, max_fight_time, game, use_medicine=False, medicine_num=0,
                 use_stone=False, stone_num=0):
        super().__init__(max_fight_time, game, use_medicine, medicine_num, use_stone, stone_num)
