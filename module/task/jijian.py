import datetime
import time

import module.step.click_step
import module.step.judge_step
import module.step.jijian_step
from module.step.jijian_step import *
from module.utils.core_control import randomClick
from module.utils.core_picture import *
from module.utils.core_template import *
from module.utils.core_email import send
from module.utils.core_config import *


@debug_recode
@timer
@func_set_timeout(timeout_time)
def clue():
    module.step.judge_step.ensureGameOpenAndInMain()
    module.step.click_step.into_jijian()
    randomClick(ui["jijian_{}_{}".format(0, 5)]["button"])
    time.sleep(sleep_time)
    if is_in_jijian_main():
        randomClick(ui["jijian_{}_{}".format(0, 5)]["button"])
        time.sleep(sleep_time)
    # 若线索交流开启中,则跳过任务
    if isClueCommunicating():
        logger.info("线索交流开启中,跳过任务")
        return
    # 进入线索交流界面
    randomClick((460, 617, 480, 640))
    time.sleep(sleep_time)
    # 关闭线索交流结束界面
    if is_template_match("/jijian/clue_communicate_end.png"):
        randomClick((37, 30, 56, 48))
        time.sleep(sleep_time)
    img = screen(memery=True)
    getClue()
    receiveClue()
    # 判断1到7号线索是否已经放置
    num = 0
    map1 = {"1": (370, 222, 412, 255), "2": (557, 260, 608, 326), "3": (766, 180, 807, 230), "4": (988, 220, 1000, 268),
            "5": (645, 479, 688, 539), "6": (850, 431, 890, 472), "7": (414, 449, 459, 505)}
    for i in range(7):
        path = "/jijian/clue_{}.png".format(i + 1)
        if is_template_match(path, screen_re=img):
            logger.info("线索{}已经放置，跳过".format(i + 1))
            num += 1
            continue
        else:
            # 选择相应线索进入
            randomClick(map1[str(i + 1)])
            time.sleep(sleep_time)
            res = anyClubCard()
            if len(res) == 0:
                randomClick((748, 564, 770, 600))
                time.sleep(sleep_time)
                continue
            elif len(res) == 5:
                x1, y1, x2, y2, s = res
                randomClick((x1, y1, x2, y2))
                num += 1
                time.sleep(sleep_time)
                # 退出选择相应线索
                randomClick((748, 564, 770, 600))
                time.sleep(sleep_time)
    # 判断能否解锁线索
    if num == 7:
        randomClick((633, 642, 693, 662))
        time.sleep(3 * sleep_time)
        # 重新进入线索交流界面
        randomClick((460, 617, 480, 640))
        time.sleep(sleep_time)
        num = 0
        for i in range(7):
            # 选择相应线索进入
            randomClick(map1[str(i + 1)])
            time.sleep(sleep_time)
            res = anyClubCard()
            if len(res) == 0:
                randomClick((748, 564, 770, 600))
                time.sleep(sleep_time)
                continue
            elif len(res) == 5:
                x1, y1, x2, y2, s = res
                randomClick((x1, y1, x2, y2))
                num += 1
                time.sleep(sleep_time)
                # 退出选择相应线索
                randomClick((748, 564, 770, 600))
                time.sleep(sleep_time)
    sendClue()
    module.step.judge_step.ensureGameOpenAndInMain()


# 基建一键收货
@debug_recode
@timer
@func_set_timeout(timeout_time)
def jijian_receive():
    module.step.judge_step.ensureGameOpenAndInMain()
    module.step.click_step.into_jijian()
    if module.step.jijian_step.is_any_notification():
        module.step.jijian_step.receive_notification()
    module.step.judge_step.ensureGameOpenAndInMain()


# 基建使用电力
@debug_recode
@timer
@func_set_timeout(timeout_time)
def use_electricity():
    module.step.judge_step.ensureGameOpenAndInMain()
    module.step.click_step.into_jijian()
    num = module.step.jijian_step.now_electricity()
    if int(num[0]) < 20:
        return
    module.step.jijian_step.use_electricity(cf.get("a"), cf.get("b"))
    module.step.judge_step.ensureGameOpenAndInMain()


# 基建排班
@debug_recode
@timer
@func_set_timeout(timeout_time_max)
def schedual():
    msgList = []
    temp = cf.read_json(project_path + "/config/schedual.json")
    schedual_dict = temp["Config"]
    data = schedual_dict["data"]
    module.step.judge_step.ensureGameOpenAndInMain()
    module.step.click_step.into_jijian()
    for i in range(len(data)):
        item = data[i]
        index = item["next_index"]
        x = item["x"]
        y = item["y"]
        type = item["type"]
        num = len(item["schedual"])
        schedual = item["schedual"][index]
        hour = schedual["hour"]
        minute = schedual["minute"]
        names = schedual["names"]
        # 判断调度时间和排班时间在1h内，执行
        if not __get_interval(hour, minute):
            continue
        msg = module.step.jijian_step.do_schedual(x, y, names, type)
        msgList.append(msg)
        logger.info("安排：" + str(names) + " 入住：" + type + " ({},{})".format(x, y))
        # 修改index为下一位
        index = (index + 1) % num
        item["next_index"] = index
    cf.write_json(temp, project_path + "/config/schedual.json")
    sum = module.step.jijian_step.auto_sleep()
    msgList.append("宿舍安排{}为干员进行休息".format(sum))
    send("排班完成", '\n'.join(msgList))
    module.step.judge_step.ensureGameOpenAndInMain()


# 判断当前时间和排班时间是否在1h内，执行
def __get_interval(hour1, minute1):
    hour = datetime.datetime.now().hour
    minute = datetime.datetime.now().minute
    if (hour1 == hour and minute >= minute1) or \
            (hour1 + 1 == hour and minute < minute1) \
            or (hour1 == 23 and hour == 0 and minute < minute1):
        flag = True
    else:
        flag = False
    return flag


if __name__ == '__main__':
    clue()
