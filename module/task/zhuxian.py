from module.step.fight_step import FightStep
from module.step.gamepass_step import GamePassStep
from module.step.common_step import CommonStep
from module.base import *


# name 主线名称    fight_time最大次数
@timer
def zhuxian(name, max_fight_time, use_medicine, medicine_num, use_stone, stone_num):
    # 将主线格式固定到 章节数-X  其中章节=实际章节 如1-X
    series = name[0]
    for i, c in enumerate(name):
        if c.isdigit():
            series = c
            break

    left = str(series) + "-X"
    v = ci[left]
    CommonStep.ensureGameOpenAndInMain()
    GamePassStep.exec_by_clickLoader(v)
    # 移动到章节最左边
    GamePassStep.goto_ahead_for_zhuxian()

    GamePassStep.find_game_position(name)
    FightStep.cycleFight(max_fight_time, name, use_medicine, medicine_num, use_stone, stone_num)
