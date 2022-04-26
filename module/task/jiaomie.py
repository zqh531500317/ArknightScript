from module.step.gamepass_step import GamePassStep
from module.step.common_step import CommonStep
from module.step.fight_step import FightStep
from module.base import *


@timer
def jiaomie(map_name, max_fight_time, use_medicine, medicine_num, use_stone, stone_num):
    CommonStep.ensureGameOpenAndInMain()

    GamePassStep.exec_by_clickLoader(ci["jiaomie"])
    num = GamePassStep.jiaomieIsFinish()

    if num > max_fight_time:
        num = max_fight_time
    time.sleep(2)
    base.randomClick((744, 359, 979, 467))
    time.sleep(base.sleep_time)
    # 开始作战
    FightStep.cycleFight(num, "剿灭", use_medicine, medicine_num, use_stone, stone_num)
