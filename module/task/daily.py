from retrying import retry
from module.step.common_step import CommonStep
from module.step.daily_step import DailyStep
from module.step.recruit_step import RecruitStep
from module.base import *


# 收货每日任务和每周任务
@my_annotation(desc="收获任务")
@before
@func_set_timeout(base.timeout_time)
def receive_renwu():
    CommonStep.ensureGameOpenAndInMain()
    CommonStep.dowait("main_renwu", "/ui/go_home.png", description="进入任务界面")
    DailyStep.receive_daily_renwu()
    DailyStep.receive_weekly_renwu()
    CommonStep.ensureGameOpenAndInMain()
    logger.info("一键领取任务完成")


# 拜访好友获取信赖
@my_annotation(desc="拜访好友")
@before
@func_set_timeout(base.timeout_time)
def friend():
    CommonStep.ensureGameOpenAndInMain()
    CommonStep.dowait("main_friend", "/friend/mingpian.png", description="点击好友按钮", retry_time=10)
    CommonStep.dowait("friend_list", "/friend/card.png", description="点击好友列表")
    CommonStep.dowait("into_friend", "/friend/in_friend_home.png", description="进入好友基建")
    DailyStep.friend_home()
    CommonStep.ensureGameOpenAndInMain()


# 商店收取信用
@my_annotation(desc="商店收取信用")
@before
@func_set_timeout(base.timeout_time)
def receive_xinyong():
    CommonStep.ensureGameOpenAndInMain()
    CommonStep.dowait("main_shop", CommonStep.isInShop, description="进入商店", retry_time=10)
    CommonStep.dowait((1125, 93, 1257, 115), "/shop/main_xinyong.png", "进入信用商店")
    base.randomClick("shop_xinyong")
    time.sleep(base.sleep_time)
    base.randomClick((686, 34, 745, 56))
    CommonStep.ensureGameOpenAndInMain()


# 购买信用商店
@my_annotation(desc="购买信用商店")
@before
@func_set_timeout(base.timeout_time)
def buy_xinyong_shop():
    # 筛选出能买的  1、没卖掉 2、不是家具零件和碳
    CommonStep.ensureGameOpenAndInMain()
    CommonStep.dowait("main_shop", CommonStep.isInShop, description="进入商店", retry_time=10)
    CommonStep.dowait((1125, 93, 1257, 115), "/shop/main_xinyong.png", "进入信用商店")
    time.sleep(base.ONE_MINUTES)
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
        img = base.screen(memery=True)
        # 买过的跳过
        a = area[i]
        s = base.cut(img, a[0], a[1], a[2], a[3])
        if base.is_template_match("/shop/sold.png", screen_re=s):
            logger.info("skip the %sst item because of sold", i + 1)
            continue
        # 不买家具零件和碳
        if len(base.template_match_best("shop/tan.png", screen_re=s)) != 0 or \
                len(base.template_match_best("shop/tansu.png", screen_re=s)) != 0 or \
                len(base.template_match_best("shop/lingjian.png", screen_re=s)) != 0:
            logger.info("skip the %sst item because of in black list", i + 1)
            continue
        ck = (buy[i][0], buy[i][1], buy[i][0] + 1, buy[i][1] + 1)
        CommonStep.dowait(ck, "/shop/buy.png", "选择购买")
        base.randomClick(mai)
        time.sleep(base.TWO_MINUTES)
        if base.is_template_match("/shop/buy.png"):
            CommonStep.dowait(bumai, "/shop/main_xinyong.png", description="无法购买:信用点数不足")
            break
        else:
            CommonStep.dowait(bumai, "/shop/main_xinyong.png", description="购买信用商店中的:{}".format("物品"))
    CommonStep.ensureGameOpenAndInMain()


# 公开招募自动刷新、选择
@my_annotation(desc="公开招募")
@before
@func_set_timeout(base.timeout_time)
def recruit_daily():
    CommonStep.ensureGameOpenAndInMain()
    CommonStep.dowait("main_recruit", "/recruit/main.png", description="进入公招界面")
    if RecruitStep.get_recruit_num() <= 3:
        logger.warn("公招卷数量少于3张，本次跳过")
        return
    RecruitStep.recruit()


# 执行连续公招任务
@my_annotation(desc="单次公开招募")
@before
def once_recruit(times):
    CommonStep.ensureGameOpenAndInMain()
    CommonStep.dowait("main_recruit", "/recruit/main.png", description="进入公招界面")
    r = -3
    for i in range(times):
        r = RecruitStep.recruit()
        if r == -2:
            break
        CommonStep.dowait("recruit_immediately", "/recruit/ensure_flash.png", description="立即招募")
        CommonStep.dowait("recruit_flash_ensure", "/recruit/main.png", description="确认招募")

    base.state.is_fight = "stop"
    CommonStep.ensureGameOpenAndInMain()
    return r


@before
@my_annotation(desc="刷芯片")
def xinpian():
    CommonStep.ensureGameOpenAndInMain()
    xinpian_1 = base.xinpian_1
    xinpian_2 = base.xinpian_2
    data, res = DailyStep.get_xinpian_info(xinpian_1, xinpian_2)
    CommonStep.ensureGameOpenAndInMain()
    DailyStep.do_xinpian(data, res)
    CommonStep.ensureGameOpenAndInMain()


@my_annotation(desc="获取理智")
@before
@func_set_timeout(base.timeout_time)
@retry
def get_lizhi():
    DailyStep.get_lizhi()


if __name__ == '__main__':
    get_lizhi()
