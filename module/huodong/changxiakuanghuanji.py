from module.huodong.base_huodong import BaseHuoDong


class ChangXiaKuangHuanJi(BaseHuoDong):
    def __init__(self, max_fight_time, game, use_medicine=False, medicine_num=0,
                 use_stone=False, stone_num=0):
        super().__init__(max_fight_time, game, use_medicine, medicine_num, use_stone, stone_num)

    @property
    def huodong_name(self):
        return "changxiakuanghuanji"

    @property
    def huodong_click(self):
        return 1058, 472, 1133, 481

    @property
    def huodongmain(self):
        return 605, 690, 625, 710, "活"

    @property
    def enter_huodong(self):
        return self.enter_huodong_template["center_one"]
