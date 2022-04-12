import time

from logzero import logger
import module.step.judge_step
import module.error.game
from module.utils.core_template import *
from module.utils.core_picture import *
from module.utils.core_control import *
from module.step.jijian_step import is_in_jijian_main


def into_jijian():
    module.step.judge_step.ensureGameOpenAndInMain()
    click(1000, 625)
    while True:
        if is_in_jijian_main():
            break
        time.sleep(sleep_time)
    logger.info("进入基建页面")


def into_main():
    if not module.step.judge_step.isInMain():
        randomClick("terminal")
        time.sleep(2 * sleep_time)
        randomClick("terminal_go_home")
        time.sleep(3 * sleep_time)
        if compareSame("go_home_from_construction"):
            randomClick("go_home_from_construction")
            time.sleep(3 * sleep_time)
        close_alert()
        # 等待直到进入主界面
        while True:
            b = module.step.judge_step.isInMain()
            if b:
                logger.info('到主界面')
                break
            time.sleep(sleep_time)


# 登录:
def into_login():
    if not isLive():
        logger.info("尝试登陆游戏")
        start()
        while True:
            time.sleep(sleep_time)
            b = module.step.judge_step.isInLogin()
            if b:
                logger.info('到登录界面')
                break
        randomClick("login")

        while True:
            time.sleep(sleep_time)
            if module.step.judge_step.isInMain():
                logger.info('到主界面')
                break
            close_alert()
    else:
        into_main()


# 关闭游戏弹框
def close_alert():
    det = template_match_best('close_ui.png')
    if len(det) != 0 and det[4] >= 0.95:
        x1 = det[0]
        y1 = det[1]
        x2 = det[2]
        y2 = det[3]
        randomClick((x1, y1, x2, y2))
        time.sleep(sleep_time)

    det = template_match_best('get_items.png', 514, 0, 758, 720)
    if len(det) != 0 and det[4] >= 0.8:
        x1 = det[0]
        y1 = det[1]
        x2 = det[2]
        y2 = det[3]
        randomClick((x1, y1, x2, y2))


def into_Fight():
    module.step.judge_step.ensureGameOpen()
    click(1150, 660)
    time.sleep(sleep_time)
    if module.step.judge_step.isInReason():
        return False
    else:
        randomClick("ensure_fight")
        logger.info("开始作战")
        return True


def out_jijian():
    click(90, 38)
    click(875, 495)
    logger.info("退出基建页面")


def out_Fight():
    click(600, 300)
    logger.info("退出奖励结算界面")


def out_fight_fail():
    randomClick((1007, 316, 1056, 340))
    time.sleep(3 * sleep_time)
    click(600, 300)


def choosedailizhihui(game):
    logger.info("启用代理指挥")
    img = screen(memery=True)
    rgb = getRGB(1060, 585, img)
    if not (rgb[0] >= 200 and rgb[1] >= 200 and rgb[2] >= 200):
        click(1060, 585)
    time.sleep(sleep_time)
    img = screen(memery=True)
    rgb = getRGB(1060, 585, img)
    if not (rgb[0] >= 200 and rgb[1] >= 200 and rgb[2] >= 200):
        raise module.error.game.CanNotChooseDaiLiZhiHui(game)


# return 1表示吃药 2表示碎石 todo 碎石
def use_medicine_or_stone(use_medicine, medicine_num, use_stone, stone_num):
    if use_medicine and medicine_num > 0:
        if compareSimilar("use_medicine_before_fight") < 0.9:
            raise module.error.game.ErrorPage()
        randomClick("use_medicine_before_fight")
        time.sleep(sleep_time)
        return 1
    # 随便点个地方退出理智补充界面
    click(1247, 500)
