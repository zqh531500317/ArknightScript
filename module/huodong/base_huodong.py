import abc
import os.path

from module.fight.base import BaseFight
from module.base import *
from module.step.common_step import CommonStep
from module.step.gamepass_step import GamePassStep
from module.utils.core_clickLoader import *
import module.error.game


class BaseHuoDong(BaseFight):
    def __init__(self, max_fight_time, game, use_medicine=False, medicine_num=0,
                 use_stone=False, stone_num=0):
        super().__init__(max_fight_time, game, use_medicine, medicine_num, use_stone, stone_num)
        self.enter_huodong_template = dict()
        self.enter_huodong_template["left"] = b_huodong[1]
        self.enter_huodong_template["center_one"] = (680, 168, 800, 200)
        self.enter_huodong_template["center_two"] = (680, 320, 800, 400)

    @abc.abstractmethod
    def huodong_name(self):
        return None

    @abc.abstractmethod
    def huodong_click(self):
        return None

    @abc.abstractmethod
    def huodongmain(self):
        return None

    @property
    def enter_huodong(self):
        return b_huodong[1]

    def enter_gamepass(self):
        CommonStep.ensureGameOpenAndInMain()
        CommonStep.dowait(a_zhongduan[1], "/ui/a_zhongduan.png", description="进入终端")
        CommonStep.dowait(self.enter_huodong,
                          OcrEntity(except_result=self.huodongmain[4],
                                    x1=self.huodongmain[0],
                                    y1=self.huodongmain[1],
                                    x2=self.huodongmain[2],
                                    y2=self.huodongmain[3]),
                          description="进入活动")
        path = base.project_path + '/asset/template/huodong/main_{}.png'.format(self.huodong_name)
        if os.path.exists(path):
            path = "/huodong/main_{}.png".format(self.huodong_name)
        else:
            path = "/huodong/main_{}.png".format("default")
        CommonStep.dowait(self.huodong_click,
                          path,
                          description="进入活动界面")
        GamePassStep.goto_ahead_for_huodong()

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
        path = base.project_path + '/asset/template/huodong/map_choosed_.png'.format(self.huodong_name)
        if os.path.exists(path):
            path = "/huodong/map_choosed_{}.png".format(self.huodong_name)
        else:
            path = "/huodong/map_choosed_{}.png".format("default")
        CommonStep.dowait(self.game_pos,
                          path,
                          description="选中关卡")
