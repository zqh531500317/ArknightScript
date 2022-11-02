from module.huodong.base_huodong import BaseHuoDong
from module.base import *
from module.step.common_step import CommonStep


class XvGuLaRen(BaseHuoDong):
    def __init__(self, max_fight_time, game, use_medicine=False, medicine_num=0,
                 use_stone=False, stone_num=0):
        super().__init__(max_fight_time, game, use_medicine, medicine_num, use_stone, stone_num)

    @property
    def huodong_name(self):
        return "xvgularen"

    @property
    def enter_huodong(self):
        return self.enter_huodong_template["left"]

    @property
    def huodong_click(self):
        return 1048, 479, 1074, 505

    @property
    def huodongmain(self):
        return 1069, 60, 1090, 79, "进"

    def find_gamepass(self):
        CommonStep.dowait((1201, 732, 1225, 391), "/huodong/xvgularen_special.png", description="进入关卡选择")
        ...

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
    from module.base import *
    from module.entity.ocr_entity import OcrEntity

    a = [1069, 60, 1090, 79, "进"]
    ocr_entity = OcrEntity(x1=a[0], y1=a[1], x2=a[2], y2=a[3], except_result=a[4])
    base.ocr(ocr_entity)
    assert ocr_entity.is_except()
