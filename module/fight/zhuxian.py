from module.fight.base import BaseFight
from module.base import *
from module.step.common_step import CommonStep
from module.step.gamepass_step import GamePassStep
import module.error.game


class ZhuXian(BaseFight):
    def __init__(self, max_fight_time, game, use_medicine=False, medicine_num=0,
                 use_stone=False, stone_num=0):
        super().__init__(max_fight_time, game, use_medicine, medicine_num, use_stone, stone_num)

    def enter_gamepass(self):
        # 将主线格式固定到 章节数-X  其中章节=实际章节 如1-X
        series = self.game[0]
        for i, c in enumerate(self.game):
            if c.isdigit():
                series = c
                break

        left = str(series) + "-X"
        v = ci[left]
        CommonStep.ensureGameOpenAndInMain()
        GamePassStep.exec_by_clickLoader(v)
        # 移动到章节最左边
        GamePassStep.goto_ahead_for_zhuxian()

    def find_gamepass(self):
        temp = []
        # 随机点击关卡的位置区域
        x1 = 0
        x2 = 0
        y1 = 0
        y2 = 0
        flag = 0
        while True:
            logger.info("尝试寻找关卡%s", self.game)
            list = GamePassStep.stage()
            if temp == list:
                flag = -1
                break
            if self.game in list:
                logger.info("识别到关卡%s", self.game)
                self.game_pos = list[self.game][0], list[self.game][1]
                return
            if flag == 1:
                break
            temp = list
            base.scroll(1000, 40, 760, 43, 200)
            time.sleep(base.sleep_time)

        if flag == -1:
            logger.error("未找到关卡%s", self.game)
            for i in range(6):
                base.scroll(600, 40, 1000, 43, 200)
                time.sleep(base.TWO_MINUTES)
            raise module.error.game.GameNotFound(self.game)
        self.game_pos = (x1, y1, x2, y2)

    def choose_gamepass(self):
        CommonStep.dowait(self.game_pos, self.isInPreFight, "选中{}".format(self.game))


if __name__ == '__main__':
    task = ZhuXian(2, "1-7", True, 0, False, 0)
    task.cycleFight()
