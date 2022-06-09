import abc

from module.base import *
import module.error.game
from module.step.common_step import CommonStep


# 未适配作战
class BaseFight:
    def __init__(self, max_fight_time, game="unknown", use_medicine=False, medicine_num=0, use_stone=False,
                 stone_num=0):
        self.game = game.upper()
        self.game_pos = None
        self.max_fight_time = max_fight_time
        self.fight_time = 0
        self.use_medicine = use_medicine
        self.medicine_num = medicine_num
        self.medicine_num_used = 0
        self.use_stone = use_stone
        self.stone_num = stone_num
        self.stone_num_used = 0
        self.ckmap = {
            "choose_daili": (1065, 603, 1068, 606),
            "start_fight": (1150, 660, 1160, 670),
            "ensure_fight": (1067, 463, 1139, 553),
            "quit_reason": (456, 25, 558, 65),
            "use_medicine_before_fight": (1073, 564, 1105, 588),
            "use_stone_before_fight": (1073, 564, 1105, 588),
            "quit_game": (600, 300, 610, 310)
        }

    def pre_cycle(self):
        pass

    def pre_fight(self):
        pass

    def enter_gamepass(self):
        pass

    def find_gamepass(self):
        pass

    def choose_gamepass(self):
        pass

    def choose_daili(self):
        if not self.isInPreFight():
            raise module.error.game.NotInPreFight(self.game)
        if base.is_template_match("/fight/map_daili_locked.png"):
            raise module.error.game.CanNotChooseDaiLiZhiHui(self.game)
        if not base.is_template_match("/fight/map_daili_choosed.png"):
            CommonStep.dowait(self.ckmap["choose_daili"], TemplateEntity("/fight/map_daili_choosed.png"), "启用代理指挥")

    def start_fight(self):
        re = CommonStep.dowait(self.ckmap["start_fight"],
                               [TemplateEntity("/fight/isInReason.png"),
                                TemplateEntity("/fight/ensure_fight.png")
                                ], description="点击开始作战"
                               )
        if re == 0:
            self.__use_medicine_and_use_stone()
            CommonStep.dowait(self.ckmap["start_fight"],
                              [TemplateEntity("/fight/isInReason.png"),
                               TemplateEntity("/fight/ensure_fight.png")
                               ], description="点击开始作战"
                              )

    @staticmethod
    def isInPreFight():
        return base.is_template_match("/fight/pre_fight.png")

    def use_medicine_fc(self):
        CommonStep.dowait(self.ckmap["use_medicine_before_fight"],
                          TemplateEntity("/fight/map_daili_choosed.png"),
                          description="当前已使用理智药{}次,最大次数为{}次".
                          format(self.medicine_num_used, self.medicine_num))

    def use_stone_fc(self):
        CommonStep.dowait(self.ckmap["use_stone_before_fight"],
                          TemplateEntity("/fight/map_daili_choosed.png"),
                          description="当前已使用源石{}次,最大次数为{}次".
                          format(self.stone_num_used, self.stone_num))

    def __use_medicine_and_use_stone(self):
        if not (self.use_medicine or self.use_stone):
            base.randomClick(self.ckmap["quit_reason"])
            raise module.error.game.NotReason(self.game)
        if self.medicine_num == self.medicine_num_used and self.stone_num == self.stone_num_used:
            base.randomClick(self.ckmap["quit_reason"])
            raise module.error.game.NotReason(self.game)
        if self.use_medicine:
            if base.is_template_match("/fight/medicine_page.png"):
                self.medicine_num_used += 1
                self.use_medicine_fc()
                return
        # todo 碎石
        if self.use_stone:
            if base.is_template_match("/fight/stone_page.png"):
                self.stone_num_used += 1
                self.use_stone_fc()
                return
        raise module.error.game.NotReason(self.game)

    def ensure_fight(self):
        CommonStep.dowait(self.ckmap["ensure_fight"], True, description="开始作战")

    def while_fight(self):
        r = CommonStep.dowait("",
                              [self.isFightEnd, self.__isFightFail, self.__isLevelUp],
                              sleep_time=base.fight_sleep_time, retry_time=base.fight_waite_time)

        if r == 1:
            self.__out_fight_fail()
            raise module.error.game.GameFail(self.game)
        elif r == 2:
            base.randomClick((635, 116, 803, 197))
            time.sleep(3)

    def isFightEnd(self):
        img = base.screen(memery=True)
        re = base.cut(img, 58, 180, 207, 256)
        res = base.ocr_without_position(re)[0]["words"]
        b = (res == '行动')
        if b:
            logger.info("战斗已结束，存储结算图片")
            time.sleep(base.get("fight_sleep_time"))
            img = base.screen(memery=True)
            path = base.save1(self.game, "get_items", img)
            if not os.path.exists(base.endFight_path[:base.endFight_path.rfind("/")]):
                os.makedirs(base.endFight_path[:base.endFight_path.rfind("/")])
            shutil.copy(path, base.endFight_path)

        else:
            logger.debug("战斗未结束")
        return b

    def __isFightFail(self):
        return base.compareSimilar("end_fight_fail") > 0.9

    def __isLevelUp(self):
        img = base.screen(memery=True)
        re = base.cut(img, 291, 351, 381, 398)
        res = base.ocr_without_position(re, None, None)[0]["words"]
        return res == "等级"

    def __out_fight_fail(self):
        base.randomClick((1007, 316, 1056, 340))
        time.sleep(3 * base.sleep_time)
        base.click(600, 300)

    def quit_fight(self):
        CommonStep.dowait(self.ckmap["quit_game"],
                          TemplateEntity("/fight/pre_fight.png"),
                          description="完成一次{}作战".format(self.game)
                          )
        self.fight_time = self.fight_time + 1

    def after(self):
        pass

    def cycleFight(self):
        self.pre_cycle()
        self.enter_gamepass()
        self.find_gamepass()
        self.choose_gamepass()
        try:
            for index in range(self.max_fight_time):
                self.fight()
            logger.info("循环作战结束,总计进行{}次{}".format(self.fight_time, self.game))
            return self.fight_time
        except module.error.game.CanNotChooseDaiLiZhiHui as e:
            e.message()
        except module.error.game.NotInPreFight as e:
            e.message()
        except module.error.game.GameFail as e:
            e.message()
        except module.error.game.NotReason as e:
            e.message()
            logger.info("循环作战结束,总计进行{}次{}".format(self.fight_time, self.game))
        except module.error.game.ErrorPage as e:
            e.message()
            logger.info("循环作战结束,总计进行{}次{}".format(self.fight_time, self.game))
            base.stop()
        finally:
            base.send("作战结束", "循环作战结束,总计进行{}次{}".format(self.fight_time, self.game))

    def fight(self):
        self.pre_fight()
        self.choose_daili()
        self.start_fight()
        self.ensure_fight()
        self.while_fight()
        self.quit_fight()
        self.after()


if __name__ == '__main__':
    task = BaseFight(2, "1-7", True, 1, False, 0)
    task.cycleFight()
