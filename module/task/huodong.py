from module.base import before
from module.huodong.yurenhao import YuRenHao


@before
def huodong(name, max_fight_time, use_medicine, medicine_num, use_stone, stone_num):
    now = "yurenhao"
    eval(now)(name, max_fight_time, use_medicine, medicine_num, use_stone, stone_num)


def yurenhao(name: str, max_fight_time, use_medicine, medicine_num, use_stone, stone_num):
    task = YuRenHao(max_fight_time, name, use_medicine, medicine_num, use_stone, stone_num)
    task.cycleFight()
