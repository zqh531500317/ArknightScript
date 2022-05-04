from module.fight.base import BaseFight
from module.base import *
from module.step.common_step import CommonStep
from module.step.gamepass_step import GamePassStep


class Ziyuanshouji(BaseFight):
    def enter_gamepass(self):
        CommonStep.ensureGameOpenAndInMain()
        # 进入资源收集区域
        time.sleep(base.sleep_time)
        base.randomClick((920, 142, 1021, 182))
        time.sleep(base.sleep_time)
        base.randomClick((706, 661, 732, 677))
        time.sleep(base.sleep_time)
        GamePassStep.find_game_position(self.game, "ziyuanshouji")

    def find_gamepass(self):
        pass

    def choose_gamepass(self):
        v = ci[self.game]
        GamePassStep.exec_by_clickLoader(v)

    def __init__(self, max_fight_time, game, use_medicine=False,
                 medicine_num=0, use_stone=False, stone_num=0):
        super().__init__(max_fight_time, game, use_medicine, medicine_num, use_stone, stone_num)
