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
    time.sleep(2)
    randomClick((920, 142, 1021, 182))
    time.sleep(2)
    randomClick((706, 661, 732, 677))
    time.sleep(2)

    try:
        # 滑到最左侧寻找
        module.step.gamepass_step.goto_ahead_for_ziyuanshouji()
        module.step.gamepass_step.find_game_position(game, "ziyuanshouji")
    except module.error.game.GameNotFound as e:
        # 滑到最右侧寻找
        module.step.gamepass_step.goto_behind_for_ziyuanshouji()
        module.step.gamepass_step.find_game_position(game, "ziyuanshouji")
    # 已经进入界面  到作战前界面
    v = ci[game]
    module.step.gamepass_step.exec_by_clickLoader(v)
