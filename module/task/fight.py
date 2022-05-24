from module.fight.base import BaseFight
from module.step.common_step import CommonStep
from module.step.fight_step import FightStep
from module.step.gamepass_step import GamePassStep
from module.base import *


# 单次作战
# return 1表示吃药 2表示碎石
def recently(name, max_fight_time, use_medicine=False, medicine_num=0, use_stone=False, stone_num=0):
    CommonStep.ensureGameOpenAndInMain()
    v = ci["recently"]
    GamePassStep.exec_by_clickLoader(v)
    FightStep.cycleFight(max_fight_time, name, use_medicine, medicine_num, use_stone, stone_num)


# 循环作战
def cycleFight(max_fight_time, game, use_medicine=False, medicine_num=0, use_stone=False, stone_num=0):
    task = BaseFight(max_fight_time, game, use_medicine, medicine_num, use_stone, stone_num)
    task.cycleFight()
