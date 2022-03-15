import time

import module.step.gamepass_step
import module.step.click_step
import module.step.judge_step
import module.task.fight
from module.utils.core_clickLoader import ci
from module.utils.core_control import *


@timer
def jiaomie(map_name, max_fight_time, use_medicine, medicine_num, use_stone, stone_num):
    module.step.judge_step.ensureGameOpenAndInMain()

    module.step.gamepass_step.exec_by_clickLoader(ci["jiaomie"])
    num = module.step.gamepass_step.jiaomieIsFinish()

    if num > max_fight_time:
        num = max_fight_time
    time.sleep(2)
    randomClick((744, 359, 979, 467))
    # 开始作战
    module.task.fight.cycleFight(num, "剿灭", use_medicine, medicine_num, use_stone, stone_num)
