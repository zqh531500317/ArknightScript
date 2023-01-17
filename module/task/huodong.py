from module.base import before
from module.huodong.changxiakuanghuanji import ChangXiaKuangHuanJi
from module.huodong.changyelinguang import ChangYeLinGuang
from module.huodong.chenyingyuyin import ChenYingYuYin
from module.huodong.fengxueguojin import FengXueGuoJin
from module.huodong.fuchaozhixia import FuChaoZhiXia
from module.huodong.lvyehuanmeng import LvYeHuanMeng
from module.huodong.xvgularen import XvGuLaRen
from module.huodong.yurenhao import YuRenHao
from module.huodong.duosuoleisi import DuoSuoLeiSi
from module.huodong.zhaowoyihuo import ZhaoWoYiHuo
from module.huodong.denglinyi import DengLinYi


@before
def huodong(name, max_fight_time, use_medicine, medicine_num, use_stone, stone_num):
    now = "denglinyi"
    eval(now)(name, max_fight_time, use_medicine, medicine_num, use_stone, stone_num)


def denglinyi(name: str, max_fight_time, use_medicine, medicine_num, use_stone, stone_num):
    task = DengLinYi(max_fight_time, name, use_medicine, medicine_num, use_stone, stone_num)
    task.cycleFight()


def zhaowoyihuo(name: str, max_fight_time, use_medicine, medicine_num, use_stone, stone_num):
    task = ZhaoWoYiHuo(max_fight_time, name, use_medicine, medicine_num, use_stone, stone_num)
    task.cycleFight()


def fengxueguojin(name: str, max_fight_time, use_medicine, medicine_num, use_stone, stone_num):
    task = FengXueGuoJin(max_fight_time, name, use_medicine, medicine_num, use_stone, stone_num)
    task.cycleFight()


def xvgularen(name: str, max_fight_time, use_medicine, medicine_num, use_stone, stone_num):
    task = XvGuLaRen(max_fight_time, name, use_medicine, medicine_num, use_stone, stone_num)
    task.cycleFight()


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
