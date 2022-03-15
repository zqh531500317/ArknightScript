import time

import module.step.judge_step
import module.step.daily_step
import module.step.recruit_step
import module.task.state
from module.utils.core_template import *
import cv2


# 收货每日任务和每周任务
@timer
@func_set_timeout(timeout_time)
def receive_renwu():
    module.step.judge_step.ensureGameOpenAndInMain()
    randomClick("main_renwu")
    time.sleep(3)
    module.step.daily_step.receive_daily_renwu()
    module.step.daily_step.receive_weekly_renwu()
    module.step.judge_step.ensureGameOpenAndInMain()
    logger.info("一键领取任务完成")


# 拜访好友获取信赖
@timer
@func_set_timeout(timeout_time)
def friend():
    module.step.judge_step.ensureGameOpenAndInMain()
    randomClick("main_friend")
    time.sleep(3)
    randomClick("friend_list")
    time.sleep(3)
    randomClick("into_friend")
    module.step.daily_step.friend_home()
    module.step.judge_step.ensureGameOpenAndInMain()


# 商店收取信用
@timer
@func_set_timeout(timeout_time)
def receive_xinyong():
    module.step.judge_step.ensureGameOpenAndInMain()
    randomClick("main_shop")
    time.sleep(3)
    randomClick((1125, 93, 1257, 115))
    time.sleep(3)
    randomClick("shop_xinyong")
    time.sleep(3)
    randomClick((686, 34, 745, 56))
    module.step.judge_step.ensureGameOpenAndInMain()


# 购买信用商店
@timer
@func_set_timeout(timeout_time)
def buy_xinyong_shop():
    # 筛选出能买的  1、没卖掉 2、不是家具零件和碳
    module.step.judge_step.ensureGameOpenAndInMain()
    randomClick("main_shop")
    time.sleep(3)
    randomClick((1125, 93, 1257, 115))
    time.sleep(3)
    buy = [(129, 266), (382, 266), (636, 266), (888, 266), (1135, 266),
           (129, 522), (382, 522), (636, 522), (888, 522), (1135, 522)]
    color = [(208, 243), (457, 242), (706, 243), (953, 237), (1211, 244),
             (200, 499), (445, 497), (702, 489), (960, 498), (1209, 490)]
    width = 237
    next = 253
    area = [
        (16, 149, 16 + width, 385),
        (16 + 1 * next, 149, 16 + 1 * next + width, 385),
        (16 + 2 * next, 149, 16 + 2 * next + width, 385),
        (16 + 3 * next, 149, 16 + 3 * next + width, 385),
        (16 + 4 * next, 149, 16 + 4 * next + width, 385),
        (16, 403, 16 + width, 639),
        (16 + 1 * next, 403, 16 + 1 * next + width, 639),
        (16 + 2 * next, 403, 16 + 2 * next + width, 639),
        (16 + 3 * next, 403, 16 + 3 * next + width, 639),
        (16 + 4 * next, 403, 16 + 4 * next + width, 639),
    ]
    bumai = (654, 16, 760, 39)
    mai = (848, 566, 957, 593)
    for i in range(10):
        screen()
        # 买过的跳过
        rgb = getRGB(color[i][0], color[i][1])
        if 100 < rgb[0] < 200 and rgb[1] < 120 and rgb[2] < 120:
            continue
        # 不买家具零件和碳
        r = cv2.imread(screen_path, 1)
        a = area[i]
        s = cut(r, a[0], a[1], a[2], a[3])
        if len(template_match_best("shop/tan.png", screen_re=s)) != 0 or \
                len(template_match_best("shop/tansu.png", screen_re=s)) != 0 or \
                len(template_match_best("shop/lingjian.png", screen_re=s)) != 0:
            continue
        click(buy[i][0], buy[i][1])
        time.sleep(2)
        randomClick(mai)
        time.sleep(2)
        screen()
        b = compareSimilar("buy_error") > 0.9
        if b:
            randomClick(bumai)
            logger.info("信用點數不足")
            break
        else:
            randomClick(bumai)
            logger.info("购买信用商店中的:%s", "物品")
    module.step.judge_step.ensureGameOpenAndInMain()


# 公开招募自动刷新、选择
@timer
@func_set_timeout(timeout_time)
def recruit_daily():
    module.step.judge_step.ensureGameOpenAndInMain()
    randomClick("main_recruit")
    time.sleep(3)
    if module.step.recruit_step.get_recruit_num() <= 3:
        logger.warn("公招卷数量少于3张，本次跳过")
        return
    module.step.recruit_step.recruit()


# 执行连续公招任务
@timer
def once_recruit(times):
    module.step.judge_step.ensureGameOpenAndInMain()
    randomClick("main_recruit")
    time.sleep(3)
    for i in range(times):
        module.step.recruit_step.recruit()
        time.sleep(2)
        randomClick("recruit_immediately")
        time.sleep(2)
        randomClick("recruit_flash_ensure")
        time.sleep(3)

    module.task.state.is_fight = "stop"
