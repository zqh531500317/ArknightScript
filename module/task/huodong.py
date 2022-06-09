from module.base import before
from module.huodong.chenyingyuyin import ChenYingYuYin
from module.huodong.fuchaozhixia import FuChaoZhiXia
from module.huodong.yurenhao import YuRenHao


@before
def huodong(name, max_fight_time, use_medicine, medicine_num, use_stone, stone_num):
    now = "chenyingyuyin"
    eval(now)(name, max_fight_time, use_medicine, medicine_num, use_stone, stone_num)


def yurenhao(name: str, max_fight_time, use_medicine, medicine_num, use_stone, stone_num):
    task = YuRenHao(max_fight_time, name, use_medicine, medicine_num, use_stone, stone_num)
    task.cycleFight()


def fuchaozhixia(name: str, max_fight_time, use_medicine, medicine_num, use_stone, stone_num):
    task = FuChaoZhiXia(max_fight_time, name, use_medicine, medicine_num, use_stone, stone_num)
    task.cycleFight()


def chenyingyuyin(name: str, max_fight_time, use_medicine, medicine_num, use_stone, stone_num):
    task = ChenYingYuYin(max_fight_time, name, use_medicine, medicine_num, use_stone, stone_num)
    task.cycleFight()
