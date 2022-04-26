import time

import module.error.game
from module.step.gamepass_step import GamePassStep
from module.step.common_step import CommonStep
from module.base import *


# name 资源本名称   fight_time最大次数
@timer
def ziyuanshouji(max_fight_time, game, use_medicine, medicine_num, use_stone, stone_num):
    findGame(game)
    # 开始作战
    module.task.fight.cycleFight(max_fight_time, game, use_medicine, medicine_num, use_stone, stone_num)


def findGame(game):
    CommonStep.ensureGameOpenAndInMain()
    # 进入资源收集区域
    time.sleep(base.sleep_time)
    base.randomClick((920, 142, 1021, 182))
    time.sleep(base.sleep_time)
    base.randomClick((706, 661, 732, 677))
    time.sleep(base.sleep_time)
    GamePassStep.find_game_position(game, "ziyuanshouji")
    v = ci[game]
    GamePassStep.exec_by_clickLoader(v)


if __name__ == '__main__':
    findGame("PR-C-2")
