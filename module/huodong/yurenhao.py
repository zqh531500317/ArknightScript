from module.huodong.base_huodong import BaseHuoDong
from module.base import *
from module.step.common_step import CommonStep
from module.step.gamepass_step import GamePassStep
import module.error.game
from module.utils.core_clickLoader import *


class YuRenHao(BaseHuoDong):
    def __init__(self, max_fight_time, game, use_medicine=False, medicine_num=0,
                 use_stone=False, stone_num=0):
        super().__init__(max_fight_time, game, use_medicine, medicine_num, use_stone, stone_num)

    @property
    def huodong_name(self):
        return "yurenhao"

    @property
    def huodong_click(self):
        # return 336, 563, 369, 570
        return 746, 181, 837, 220

    def find_gamepass(self):
        SN_9 = (687, 404, 712, 428)
        SN_10 = (750, 297, 779, 322)
        if self.game.upper() == "SN-9":
            self.game_pos = SN_9
        elif self.game.upper() == "SN-10":
            self.game_pos = SN_10

    @staticmethod
    def isInPreFight():
        return base.is_template_match("/huodong/map_choosed_yurenhao.png")

    def choose_daili(self):
        if not base.is_template_match("/huodong/map_daili_{}.png".format(self.huodong_name)):
            CommonStep.dowait((1085, 582, 1086, 583),
                              "/huodong/map_daili_{}.png".format(self.huodong_name),
                              description="选中代理")

    def quit_fight(self):
        CommonStep.dowait(self.ckmap["quit_game"],
                          TemplateEntity("/huodong/map_daili_yurenhao.png"),
                          description="完成一次{}作战".format(self.game)
                          )
        self.fight_time = self.fight_time + 1

    def use_medicine_fc(self):
        CommonStep.dowait(self.ckmap["use_medicine_before_fight"],
                          TemplateEntity("/huodong/map_daili_yurenhao.png"),
                          description="当前已使用理智药{}次,最大次数为{}次".
                          format(self.medicine_num_used, self.medicine_num))


if __name__ == '__main__':
    task = YuRenHao(99, "SN-9")
    task.cycleFight()
