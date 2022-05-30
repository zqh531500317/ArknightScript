from module.base import before
from module.huodong.fuchaozhixia import FuChaoZhiXia
from module.huodong.yurenhao import YuRenHao


@before
def huodong(name, max_fight_time, use_medicine, medicine_num, use_stone, stone_num):
    now = "fuchaozhixia"
    eval(now)(name, max_fight_time, use_medicine, medicine_num, use_stone, stone_num)


def yurenhao(name: str, max_fight_time, use_medicine, medicine_num, use_stone, stone_num):
    task = YuRenHao(max_fight_time, name, use_medicine, medicine_num, use_stone, stone_num)
    task.cycleFight()


def fuchaozhixia(name: str, max_fight_time, use_medicine, medicine_num, use_stone, stone_num):
    task = FuChaoZhiXia(max_fight_time, name, use_medicine, medicine_num, use_stone, stone_num)
    task.cycleFight()
