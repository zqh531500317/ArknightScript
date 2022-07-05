from module.huodong.base_huodong import BaseHuoDong


class LvYeHuanMeng(BaseHuoDong):
    @property
    def huodong_name(self):
        return "lvyehuanmeng"

    @property
    def huodong_click(self):
        return 1126, 272, 1157, 284

    @property
    def huodongmain(self):
        return 1055, 29, 1100, 52, "查看"

    def __init__(self, max_fight_time, game, use_medicine=False, medicine_num=0,
                 use_stone=False, stone_num=0):
        super().__init__(max_fight_time, game, use_medicine, medicine_num, use_stone, stone_num)


if __name__ == '__main__':
    task = LvYeHuanMeng(1, "DV-8")
    task.cycleFight()
