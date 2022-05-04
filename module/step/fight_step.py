from module.base import *
from module.step.common_step import CommonStep
import module.error.game


class FightStep:

    # 单次作战
    # return 1表示吃药 2表示碎石
    @staticmethod
    def fight(game, use_medicine=False, medicine_num=0, use_stone=False, stone_num=0,
              ignore_prefight=False, ignore_daili=False, prefunc=None, *parem):
        if prefunc is not None:
            prefunc(*parem)
        if not ignore_prefight:
            if not CommonStep.isInPreFight():
                raise module.error.game.NotInPreFight(game)
        if not ignore_daili:
            CommonStep.choosedailizhihui(game)
        r = 0
        # todo 碎石
        b = CommonStep.into_Fight()

        if not b:
            if not (use_medicine or use_stone):
                base.randomClick((456, 25, 558, 65))
                raise module.error.game.NotReason(game)
            if medicine_num == 0 and stone_num == 0:
                base.randomClick((456, 25, 558, 65))
                raise module.error.game.NotReason(game)
            r = CommonStep.use_medicine_or_stone(use_medicine, medicine_num, use_stone, stone_num)
            if r == 1 or r == 2:
                CommonStep.into_Fight()
        while True:
            time.sleep(base.fight_sleep_time)
            if CommonStep.isFightEnd(game):
                break
            # 若关卡失败
            if CommonStep.isFightFail():
                CommonStep.out_fight_fail()
                raise module.error.game.GameFail(game)
            # 若升级
            if CommonStep.isLevelUp():
                base.randomClick((635, 116, 803, 197))
                time.sleep(3)
                break
        CommonStep.out_Fight()
        logger.info("完成一次{}作战".format(game))
        return r

    # 循环作战
    @staticmethod
    def cycleFight(max_fight_time, game, use_medicine=False, medicine_num=0,
                   use_stone=False, stone_num=0, ignore_prefight=False,
                   ignore_daili=False, prefunc=None, *parem):
        fight_time = 0
        try:
            for index in range(max_fight_time):
                time.sleep(base.fight_sleep_time)
                r = FightStep.fight(game, use_medicine, medicine_num, use_stone,
                                    stone_num, ignore_prefight, ignore_daili, prefunc, *parem)
                fight_time = fight_time + 1
                if r == 1:
                    medicine_num = medicine_num - 1
                if r == 2:
                    stone_num = stone_num - 1
            logger.info("循环作战结束,总计进行{}次{}".format(fight_time, game))
            return fight_time
        except module.error.game.CanNotChooseDaiLiZhiHui as e:
            e.message()
        except module.error.game.NotInPreFight as e:
            e.message()
        except module.error.game.GameFail as e:
            e.message()
        except module.error.game.NotReason as e:
            e.message()
            logger.info("循环作战结束,总计进行{}次{}".format(fight_time, game))
        except module.error.game.ErrorPage as e:
            e.message()
            logger.info("循环作战结束,总计进行{}次{}".format(fight_time, game))
            base.stop()
        finally:
            base.send("作战结束", "循环作战结束,总计进行{}次{}".format(fight_time, game))
