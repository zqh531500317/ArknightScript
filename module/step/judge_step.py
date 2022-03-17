from logzero import logger
import module.step.click_step
from module.utils.core_template import *
import shutil


def isInLogin():
    ensureGameOpen()
    return compareSimilar("login") > 0.9


def isFightEnd(game):
    time.sleep(3)
    if game == "剿灭":
        b = compareSimilar("end_jiaomie")
        if b > 0.8:
            randomClick("end_jiaomie")
            time.sleep(3)
            logger.info("战斗已结束，存储结算图片")
            screen()
            path = save1("jiaomie", "get_items")
            shutil.copy(path, endFight_path)
        else:
            logger.debug("战斗未结束")
        return b > 0.8
    else:
        b = compareAllWhile("end_fight")
        if b:
            logger.info("战斗已结束，存储结算图片")
            screen()
            path = save1(game, "get_items")
            shutil.copy(path, endFight_path)

        else:
            logger.debug("战斗未结束")
        return b


def isFightFail():
    return compareSimilar("end_fight_fail") > 0.9


def isLevelUp():
    rgb = getRGB(234, 414)
    if rgb[0] == 255 and rgb[1] == 255 and rgb[2] == 255:
        return True
    else:
        return False


def isInMain():
    ensureGameOpen()
    return compareSimilar("main") > 0.9


def isInMessageAfterLogin():
    ensureGameOpen()
    return compareSame("message_after_login")


def isInMonthAfterLogin():
    ensureGameOpen()
    return compareSimilar("month_after_login") > 0.9


def isInTerminal():
    ensureGameOpen()
    return compareSame("terminal")


# 是否在理智恢复界面
def isInReason():
    ensureGameOpen()
    if compareSimilar("has_reason_before_fight") > 0.9:
        return False
    else:
        return True


# 是否在作战前界面
def isInPreFight():
    ensureGameOpen()
    return compareSimilar("pre_fight") > 0.7


def ensureGameOpen():
    if not isLive():
        module.step.click_step.into_login()


def ensureGameOpenAndInMain():
    module.step.click_step.into_login()
