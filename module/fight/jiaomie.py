from module.fight.base import BaseFight
from module.base import *
from module.step.common_step import CommonStep
from module.step.gamepass_step import GamePassStep


class Jiaomie(BaseFight):

    # def isInWeiTuo(self):
    #     return base.is_template_match("/fight/jiaomie_weituo.png")

    def enter_gamepass(self):
        CommonStep.ensureGameOpenAndInMain()

        GamePassStep.exec_by_clickLoader(ci["jiaomie"])
        num = GamePassStep.jiaomieIsFinish()

        self.max_fight_time = min(self.max_fight_time, num)
        time.sleep(2)
        base.randomClick((744, 359, 979, 467))
        time.sleep(base.sleep_time)

    def fight(self):
        # 点击开始行动
        CommonStep.dowait(self.ckmap["start_fight"],
                          base.is_template_match("/fight/jiaomie_ensure_use.png"),
                          description="点击开始行动")
        # 点击确认使用
        CommonStep.dowait(self.ckmap["ensure_use"],
                          self.isFightEnd,
                          description="点击确认使用")
        self.quit_fight()

    def cycleFight(self):
        self.enter_gamepass()
        if not base.is_template_match("/fight/jiaomie_weituo_choosed.png"):
            # 点击全权委托
            CommonStep.dowait(self.ckmap["weituo"],
                              base.is_template_match("/fight/jiaomie_weituo_choosed.png"),
                              description="点击全权委托")
        for i in range(self.max_fight_time):
            self.fight()

    def __init__(self, max_fight_time, game="jiaomie", use_medicine=False,
                 medicine_num=0, use_stone=False, stone_num=0):
        super().__init__(max_fight_time, game, use_medicine, medicine_num, use_stone, stone_num)
        self.ckmap["weituo"] = (960, 590, 970, 595)
        self.ckmap["ensure_use"] = (1100, 645, 1180, 670)


if __name__ == '__main__':
    task = Jiaomie(5)
    task.cycleFight()
