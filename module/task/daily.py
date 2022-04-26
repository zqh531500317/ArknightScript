from module.base import *
from module.step.common_step import CommonStep

# 收货每日任务和每周任务
from module.step.daily_step import DailyStep
from module.step.recruit_step import RecruitStep
from module.utils.core_assetLoader import ui
from module.utils.core_clickLoader import ci


@debug_recode
@timer
@func_set_timeout(base.timeout_time)
def receive_renwu():
    CommonStep.ensureGameOpenAndInMain()
    CommonStep.dowait("main_renwu", "/ui/go_home.png", description="进入任务界面")
    DailyStep.receive_daily_renwu()
    DailyStep.receive_weekly_renwu()
    CommonStep.ensureGameOpenAndInMain()
    logger.info("一键领取任务完成")


# 拜访好友获取信赖
@debug_recode
@timer
@func_set_timeout(base.timeout_time)
def friend():
    CommonStep.ensureGameOpenAndInMain()
    CommonStep.dowait("main_friend", "/friend/mingpian.png", description="点击好友按钮")
    CommonStep.dowait("friend_list", "/friend/card.png", description="点击好友列表")
    CommonStep.dowait("into_friend", "/friend/in_friend_home.png", description="进入好友基建")
    DailyStep.friend_home()
    CommonStep.ensureGameOpenAndInMain()


# 商店收取信用
@debug_recode
@timer
@func_set_timeout(base.timeout_time)
def receive_xinyong():
    CommonStep.ensureGameOpenAndInMain()
    base.randomClick("main_shop")
    time.sleep(base.sleep_time)
    base.randomClick((1125, 93, 1257, 115))
    time.sleep(base.sleep_time)
    base.randomClick("shop_xinyong")
    time.sleep(base.sleep_time)
    base.randomClick((686, 34, 745, 56))
    CommonStep.ensureGameOpenAndInMain()


# 购买信用商店
@debug_recode
@timer
@func_set_timeout(base.timeout_time)
def buy_xinyong_shop():
    # 筛选出能买的  1、没卖掉 2、不是家具零件和碳
    CommonStep.ensureGameOpenAndInMain()
    base.randomClick("main_shop")
    time.sleep(base.sleep_time)
    base.randomClick((1125, 93, 1257, 115))
    time.sleep(base.sleep_time)
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
        rgb = base.get_rgb(color[i][0], color[i][1], img_path=img)
        if 100 < rgb[0] < 200 and rgb[1] < 120 and rgb[2] < 120:
            continue
        # 不买家具零件和碳
        a = area[i]
        s = base.cut(img, a[0], a[1], a[2], a[3])
        if len(base.template_match_best("shop/tan.png", screen_re=s)) != 0 or \
                len(base.template_match_best("shop/tansu.png", screen_re=s)) != 0 or \
                len(base.template_match_best("shop/lingjian.png", screen_re=s)) != 0:
            continue
        base.click(buy[i][0], buy[i][1])
        time.sleep(base.sleep_time)
        base.randomClick(mai)
        time.sleep(base.sleep_time)
        b = base.compareSimilar("buy_error") > 0.9
        if b:
            base.randomClick(bumai)
            logger.info("信用點數不足")
            break
        else:
            base.randomClick(bumai)
            logger.info("购买信用商店中的:%s", "物品")
    CommonStep.ensureGameOpenAndInMain()


# 公开招募自动刷新、选择
@debug_recode
@timer
@func_set_timeout(base.timeout_time)
def recruit_daily():
    CommonStep.ensureGameOpenAndInMain()
    CommonStep.dowait("main_recruit", "/recruit/main.png", description="进入公招界面")
    if RecruitStep.get_recruit_num() <= 3:
        logger.warn("公招卷数量少于3张，本次跳过")
        return
    RecruitStep.recruit()


# 执行连续公招任务
@debug_recode
@timer
def once_recruit(times):
    CommonStep.ensureGameOpenAndInMain()
    CommonStep.dowait("main_recruit", "/recruit/main.png", description="进入公招界面")
    for i in range(times):
        RecruitStep.recruit()
        time.sleep(base.sleep_time)
        base.randomClick("recruit_immediately")
        time.sleep(base.sleep_time)
        base.randomClick("recruit_flash_ensure")
        time.sleep(base.sleep_time)
    base.state.is_fight = "stop"


@debug_recode
@timer
def xinpian():
    CommonStep.ensureGameOpenAndInMain()
    xinpian_1 = base.xinpian_1
    xinpian_2 = base.xinpian_2
    data, res = DailyStep.get_xinpian_info(xinpian_1, xinpian_2)
    CommonStep.ensureGameOpenAndInMain()
    DailyStep.do_xinpian(data, res)
    CommonStep.ensureGameOpenAndInMain()


@debug_recode
@func_set_timeout(base.timeout_time)
@timer
def get_lizhi():
    CommonStep.ensureGameOpenAndInMain()
    time.sleep(1)
    CommonStep.exec_by_clickLoader(ci["lizhi"])
    time.sleep(base.sleep_time)
    region = base.screen(memery=True)
    lizhi_before_fight = ui["lizhi_before_fight"]["area"]
    x1, y1, x2, y2 = lizhi_before_fight
    cropped = base.cut(region, x1, y1, x2, y2)
    result = base.ocr_without_position(cropped, cand_alphabet=base.number_tag)
    logger.debug("获取理智内容是：" + str(result))
    dic = result[0]["words"].split("/")
    base.state.lizhi["time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    base.state.lizhi["lizhi"] = dic[0]
    base.state.lizhi["maxlizhi"] = dic[1]
    CommonStep.ensureGameOpenAndInMain()


if __name__ == '__main__':
    friend()
