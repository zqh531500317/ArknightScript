import time

import module.step.judge_step
import module.step.daily_step
import module.step.recruit_step
import module.task.state
from module.utils.core_config import timer, func_set_timeout, cf, logger, debug_recode
from module.utils.core_template import template_match_best
from module.utils.core_control import randomClick, screen, click
from module.utils.core_picture import cut, getRGB, compareSimilar
from module.step.click_step import dowait


# 收货每日任务和每周任务
@debug_recode
@timer
@func_set_timeout(cf.timeout_time)
def receive_renwu():
    module.step.judge_step.ensureGameOpenAndInMain()
    randomClick("main_renwu")
    time.sleep(cf.sleep_time)
    module.step.daily_step.receive_daily_renwu()
    module.step.daily_step.receive_weekly_renwu()
    module.step.judge_step.ensureGameOpenAndInMain()
    logger.info("一键领取任务完成")


# 拜访好友获取信赖
@debug_recode
@timer
@func_set_timeout(cf.timeout_time)
def friend():
    module.step.judge_step.ensureGameOpenAndInMain()
    dowait("main_friend", "/friend/mingpian.png")
    dowait("friend_list", "/friend/card.png")
    time.sleep(2 * cf.sleep_time)
    randomClick("into_friend")
    module.step.daily_step.friend_home()
    module.step.judge_step.ensureGameOpenAndInMain()


# 商店收取信用
@debug_recode
@timer
@func_set_timeout(cf.timeout_time)
def receive_xinyong():
    module.step.judge_step.ensureGameOpenAndInMain()
    randomClick("main_shop")
    time.sleep(cf.sleep_time)
    randomClick((1125, 93, 1257, 115))
    time.sleep(cf.sleep_time)
    randomClick("shop_xinyong")
    time.sleep(cf.sleep_time)
    randomClick((686, 34, 745, 56))
    module.step.judge_step.ensureGameOpenAndInMain()


# 购买信用商店
@debug_recode
@timer
@func_set_timeout(cf.timeout_time)
def buy_xinyong_shop():
    # 筛选出能买的  1、没卖掉 2、不是家具零件和碳
    module.step.judge_step.ensureGameOpenAndInMain()
    randomClick("main_shop")
    time.sleep(cf.sleep_time)
    randomClick((1125, 93, 1257, 115))
    time.sleep(cf.sleep_time)
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
        img = screen(memery=True)
        # 买过的跳过
        rgb = getRGB(color[i][0], color[i][1], img_path=img)
        if 100 < rgb[0] < 200 and rgb[1] < 120 and rgb[2] < 120:
            continue
        # 不买家具零件和碳
        a = area[i]
        s = cut(img, a[0], a[1], a[2], a[3])
        if len(template_match_best("shop/tan.png", screen_re=s)) != 0 or \
                len(template_match_best("shop/tansu.png", screen_re=s)) != 0 or \
                len(template_match_best("shop/lingjian.png", screen_re=s)) != 0:
            continue
        click(buy[i][0], buy[i][1])
        time.sleep(cf.sleep_time)
        randomClick(mai)
        time.sleep(cf.sleep_time)
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
@debug_recode
@timer
@func_set_timeout(cf.timeout_time)
def recruit_daily():
    module.step.judge_step.ensureGameOpenAndInMain()
    randomClick("main_recruit")
    time.sleep(cf.sleep_time)
    if module.step.recruit_step.get_recruit_num() <= 3:
        logger.warn("公招卷数量少于3张，本次跳过")
        return
    module.step.recruit_step.recruit()


# 执行连续公招任务
@debug_recode
@timer
def once_recruit(times):
    module.step.judge_step.ensureGameOpenAndInMain()
    randomClick("main_recruit")
    time.sleep(cf.sleep_time)
    for i in range(times):
        module.step.recruit_step.recruit()
        time.sleep(cf.sleep_time)
        randomClick("recruit_immediately")
        time.sleep(cf.sleep_time)
        randomClick("recruit_flash_ensure")
        time.sleep(cf.sleep_time)

    module.task.state.is_fight = "stop"


@debug_recode
@timer
def xinpian():
    module.step.judge_step.ensureGameOpenAndInMain()
    xinpian_1 = cf.xinpian_1
    xinpian_2 = cf.xinpian_2
    data, res = module.step.daily_step.get_xinpian_info(xinpian_1, xinpian_2)
    module.step.judge_step.ensureGameOpenAndInMain()
    module.step.daily_step.do_xinpian(data, res)
    module.step.judge_step.ensureGameOpenAndInMain()


if __name__ == '__main__':
    xinpian()
