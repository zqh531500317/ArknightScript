import time

import module.error.game
import module.step.click_step
import module.step.judge_step
from module.utils.core_picture import *
from module.utils.core_email import *
from module.utils.core_clickLoader import ci


# 单次作战
# return 1表示吃药 2表示碎石
def fight(game, use_medicine, medicine_num, use_stone, stone_num):
    if not module.step.judge_step.isInPreFight():
        raise module.error.game.NotInPreFight(game)
    module.step.click_step.choosedailizhihui(game)
    r = 0
    # todo 碎石
    b = module.step.click_step.into_Fight()

    if not b:
        if not (use_medicine or use_stone):
            randomClick((456, 25, 558, 65))
            raise module.error.game.NotReason(game)
        if medicine_num == 0 and stone_num == 0:
            randomClick((456, 25, 558, 65))
            raise module.error.game.NotReason(game)
        r = module.step.click_step.use_medicine_or_stone(use_medicine, medicine_num, use_stone, stone_num)
        if r == 1 or r == 2:
            module.step.click_step.into_Fight()
    while True:
        time.sleep(10)
        if module.step.judge_step.isFightEnd(game):
            break
        # 若关卡失败
        if module.step.judge_step.isFightFail():
            module.step.click_step.out_fight_fail()
            raise module.error.game.GameFail(game)
        # 若升级
        if module.step.judge_step.isLevelUp():
            randomClick((635, 116, 803, 197))
            time.sleep(3)
            break
    module.step.click_step.out_Fight()
    logger.info("完成一次{}作战".format(game))
    return r


# 循环作战
def cycleFight(max_fight_time, game, use_medicine, medicine_num, use_stone, stone_num):
    fight_time = 0
    try:
        for index in range(max_fight_time):
            time.sleep(8)
            r = fight(game, use_medicine, medicine_num, use_stone, stone_num)
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
        stop()
    finally:
        send("作战结束", "循环作战结束,总计进行{}次{}".format(fight_time, game))


def recently(name, max_fight_time, use_medicine, medicine_num, use_stone, stone_num):
    module.step.judge_step.ensureGameOpenAndInMain()
    v = ci["recently"]
    module.step.gamepass_step.exec_by_clickLoader(v)
    module.task.fight.cycleFight(max_fight_time, name, use_medicine, medicine_num, use_stone, stone_num)
