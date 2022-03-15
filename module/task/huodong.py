import time

import module.step.gamepass_step
import module.step.click_step
import module.step.judge_step
import module.task.fight
from module.utils.core_clickLoader import ci
from module.utils.core_control import *


def huodong(name, max_fight_time, use_medicine, medicine_num, use_stone, stone_num):
    now = "wudaoxianlu"
    eval(now)(name, max_fight_time, use_medicine, medicine_num, use_stone, stone_num)


# name 名称    fight_time最大次数
def wudaoxianlu(name, max_fight_time, use_medicine, medicine_num, use_stone, stone_num):
    module.step.judge_step.ensureGameOpenAndInMain()
    v = ci["huodong"]
    module.step.gamepass_step.exec_by_clickLoader(v)
    randomClick((1114, 465, 1130, 482))
    time.sleep(sleep_time)
    # 移动到章节最右边
    module.step.gamepass_step.goto_behind_for_huodong()
    if name == "GA-6":
        randomClick((34, 332, 95, 350))
    elif name == "GA-7":
        randomClick((317, 332, 382, 350))
    elif name == "GA-8":
        randomClick((612, 332, 678, 350))
    else:
        return
    time.sleep(sleep_time)
    module.task.fight.cycleFight(max_fight_time, name, use_medicine, medicine_num, use_stone, stone_num)


# name 名称    fight_time最大次数
def changyelinguang(name, max_fight_time, use_medicine, medicine_num, use_stone, stone_num):
    module.step.judge_step.ensureGameOpenAndInMain()
    v = ci["changyelinguang"]
    module.step.gamepass_step.exec_by_clickLoader(v)
    # 移动到章节最左边
    module.step.gamepass_step.goto_ahead_for_huodong()

    module.step.gamepass_step.find_game_position(name)
    module.task.fight.cycleFight(max_fight_time, name, use_medicine, medicine_num, use_stone, stone_num)


# name 名称    fight_time最大次数
def gudaofengyun(name, max_fight_time, use_medicine, medicine_num, use_stone, stone_num):
    module.step.judge_step.ensureGameOpenAndInMain()
    v = ci["gudaofengyun"]
    module.step.gamepass_step.exec_by_clickLoader(v)
    time.sleep(3)
    if name == "MB-6":
        randomClick((804, 386, 873, 409))
    elif name == "MB-7":
        randomClick((802, 512, 876, 534))
    elif name == "MB-8":
        randomClick((1102, 513, 1170, 536))
    else:
        return
    time.sleep(3)
    module.task.fight.cycleFight(max_fight_time, name, use_medicine, medicine_num, use_stone, stone_num)


# name 名称    fight_time最大次数
def fengxueguojing(name, max_fight_time, use_medicine, medicine_num, use_stone, stone_num):
    module.step.judge_step.ensureGameOpenAndInMain()
    v = ci["fengxueguojing"]
    module.step.gamepass_step.exec_by_clickLoader(v)
    time.sleep(3)
    module.step.gamepass_step.goto_behind_for_ziyuanshouji()
    time.sleep(3)
    if name == "BI-6":
        randomClick((228, 194, 295, 213))
    elif name == "BI-7":
        randomClick((447, 280, 506, 300))
    elif name == "BI-8":
        randomClick((000, 384, 670, 402))
    else:
        return
    time.sleep(3)
    module.task.fight.cycleFight(max_fight_time, name, use_medicine, medicine_num, use_stone, stone_num)


# name 名称    fight_time最大次数
def huazhongren(name, max_fight_time, use_medicine, medicine_num, use_stone, stone_num):
    module.step.judge_step.ensureGameOpenAndInMain()
    v = ci["huazhongren"]
    module.step.gamepass_step.exec_by_clickLoader(v)
    # 移动到章节最左边
    module.step.gamepass_step.goto_ahead_for_huodong()

    module.step.gamepass_step.find_game_position(name)
    module.task.fight.cycleFight(max_fight_time, name, use_medicine, medicine_num, use_stone, stone_num)


# name 名称    fight_time最大次数
def jiangjinjiu(name, max_fight_time, use_medicine, medicine_num, use_stone, stone_num):
    module.step.judge_step.ensureGameOpenAndInMain()
    v = ci["jiangjinjiu"]
    module.step.gamepass_step.exec_by_clickLoader(v)

    if name != "IW-6" and name != "IW-7" and name != "IW-8":
        return
        # 移动到章节最左边
    module.step.gamepass_step.goto_ahead_for_huodong()

    module.step.gamepass_step.find_game_position_with_template(name)
    module.task.fight.cycleFight(max_fight_time, name, use_medicine, medicine_num, use_stone, stone_num)
