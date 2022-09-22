from module.base import before
from module.huodong.changxiakuanghuanji import ChangXiaKuangHuanJi
from module.huodong.changyelinguang import ChangYeLinGuang
from module.huodong.chenyingyuyin import ChenYingYuYin
from module.huodong.fuchaozhixia import FuChaoZhiXia
from module.huodong.lvyehuanmeng import LvYeHuanMeng
from module.huodong.yurenhao import YuRenHao
from module.huodong.duosuoleisi import DuoSuoLeiSi


@before
def huodong(name, max_fight_time, use_medicine, medicine_num, use_stone, stone_num):
    now = "changyelinguang"
    eval(now)(name, max_fight_time, use_medicine, medicine_num, use_stone, stone_num)


def changyelinguang(name: str, max_fight_time, use_medicine, medicine_num, use_stone, stone_num):
    task = ChangYeLinGuang(max_fight_time, name, use_medicine, medicine_num, use_stone, stone_num)
    task.cycleFight()


def changxiakuanghuanji(name: str, max_fight_time, use_medicine, medicine_num, use_stone, stone_num):
    task = ChangXiaKuangHuanJi(max_fight_time, name, use_medicine, medicine_num, use_stone, stone_num)
    task.cycleFight()


def yurenhao(name: str, max_fight_time, use_medicine, medicine_num, use_stone, stone_num):
    task = YuRenHao(max_fight_time, name, use_medicine, medicine_num, use_stone, stone_num)
    task.cycleFight()


def fuchaozhixia(name: str, max_fight_time, use_medicine, medicine_num, use_stone, stone_num):
    task = FuChaoZhiXia(max_fight_time, name, use_medicine, medicine_num, use_stone, stone_num)
    task.cycleFight()


def chenyingyuyin(name: str, max_fight_time, use_medicine, medicine_num, use_stone, stone_num):
    task = ChenYingYuYin(max_fight_time, name, use_medicine, medicine_num, use_stone, stone_num)
    task.cycleFight()


def lvyehuanmeng(name: str, max_fight_time, use_medicine, medicine_num, use_stone, stone_num):
    task = LvYeHuanMeng(max_fight_time, name, use_medicine, medicine_num, use_stone, stone_num)
    task.cycleFight()


def duosuoleisi(name: str, max_fight_time, use_medicine, medicine_num, use_stone, stone_num):
    task = DuoSuoLeiSi(max_fight_time, name, use_medicine, medicine_num, use_stone, stone_num)
    task.cycleFight()
