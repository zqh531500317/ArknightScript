import os.path
import module.step.click_step
from module.utils.core_template import *
from module.utils.core_picture import *
from module.utils.core_control import *
import shutil
from module.utils.core_ocr import ocr_without_position


def isInLogin():
    img = screen(memery=True)
    return is_template_match("isLogining.png", screen_re=img, template_threshold=0.9)


def isFightEnd(game):
    time.sleep(cf.get("sleep_time"))
    if game == "剿灭":
        b = is_template_match("/fight/end_jiaomie.png")
        if b:
            randomClick("end_jiaomie")
            time.sleep(cf.get("sleep_time"))
            logger.info("战斗已结束，存储结算图片")
            img = screen(memery=True)
            path = save1("jiaomie", "get_items", img)
            if not os.path.exists(cf.endFight_path[:cf.endFight_path.rfind("/")]):
                os.makedirs(cf.endFight_path[:cf.endFight_path.rfind("/")])
            shutil.copy(path, cf.endFight_path)
        else:
            logger.debug("战斗未结束")
        return b > 0.8
    else:
        img = screen(memery=True)
        re = cut(img, 58, 180, 207, 256)
        res = ocr_without_position(re)[0]["words"]
        b = (res == '行动')
        if b:
            logger.info("战斗已结束，存储结算图片")
            time.sleep(cf.get("sleep_time") * 2)
            img = screen(memery=True)
            path = save1(game, "get_items", img)
            if not os.path.exists(cf.endFight_path[:cf.endFight_path.rfind("/")]):
                os.makedirs(cf.endFight_path[:cf.endFight_path.rfind("/")])
            shutil.copy(path, cf.endFight_path)

        else:
            logger.debug("战斗未结束")
        return b


def isFightFail():
    return compareSimilar("end_fight_fail") > 0.9


def isLevelUp():
    img = screen(memery=True)
    re = cut(img, 291, 351, 381, 398)
    res = ocr_without_position(re, None, None)[0]["words"]
    return res == "等级"


def isInMain():
    return is_template_match("/ui/main.png")


def isInMessageAfterLogin():
    return compareSame("message_after_login")


def isInMonthAfterLogin():
    return compareSimilar("month_after_login") > 0.9


def isInTerminal():
    return compareSame("terminal")


# 是否在理智恢复界面
def isInReason():
    return is_template_match("isInReason.png")


# 是否在作战前界面
def isInPreFight():
    return is_template_match("pre_fight.png")


def ensureGameOpen():
    if not isLive():
        module.step.click_step.into_login()


def ensureGameOpenAndInMain():
    module.step.click_step.into_login()


if __name__ == '__main__':
    ensureGameOpenAndInMain()
