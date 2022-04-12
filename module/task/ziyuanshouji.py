import time

import module.error.game
import module.step.gamepass_step
import module.step.click_step
import module.step.judge_step
import module.task.fight
from module.utils.core_clickLoader import ci
from module.utils.core_control import *


# name 资源本名称   fight_time最大次数
@timer
def ziyuanshouji(max_fight_time, game, use_medicine, medicine_num, use_stone, stone_num):
    findGame(game)
    # 开始作战
    module.task.fight.cycleFight(max_fight_time, game, use_medicine, medicine_num, use_stone, stone_num)


def findGame(game):
    module.step.judge_step.ensureGameOpenAndInMain()
    # 进入资源收集区域
    time.sleep(sleep_time)
    randomClick((920, 142, 1021, 182))
    time.sleep(sleep_time)
    randomClick((706, 661, 732, 677))
    time.sleep(sleep_time)
    module.step.gamepass_step.find_game_position(game, "ziyuanshouji")
    v = ci[game]
    module.step.gamepass_step.exec_by_clickLoader(v)


if __name__ == '__main__':
    findGame("PR-C-2")
