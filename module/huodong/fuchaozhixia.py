from module.huodong.base_huodong import BaseHuoDong


class FuChaoZhiXia(BaseHuoDong):
    def __init__(self, max_fight_time, game, use_medicine=False, medicine_num=0,
                 use_stone=False, stone_num=0):
        super().__init__(max_fight_time, game, use_medicine, medicine_num, use_stone, stone_num)

    @property
    def huodong_name(self):
        return "fuchaozhixia"

    @property
    def huodong_click(self):
        return 1099, 440, 1150, 449

    @property
    def huodongmain(self):
        return 892, 83, 932, 105, "作战"
