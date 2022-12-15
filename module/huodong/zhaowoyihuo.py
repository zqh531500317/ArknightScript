from module.huodong.base_huodong import BaseHuoDong


class ZhaoWoYiHuo(BaseHuoDong):
    def __init__(self, max_fight_time, game, use_medicine=False, medicine_num=0,
                 use_stone=False, stone_num=0):
        super().__init__(max_fight_time, game, use_medicine, medicine_num, use_stone, stone_num)

    @property
    def huodong_name(self):
        return "zhaowoyihuo"

    @property
    def huodong_click(self):
        return 1138, 464, 1172, 491

    @property
    def huodongmain(self):
        return 899, 34, 919, 54, "查"

    @property
    def enter_huodong(self):
        return self.enter_huodong_template["left"]
