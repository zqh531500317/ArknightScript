import copy
import datetime
import os.path
import time

from module.step.common_step import CommonStep
from module.step.jijian_step import JiJianStep
from module.base import *


@my_annotation(desc="线索交流")
@before
@func_set_timeout(base.timeout_time)
def clue():
    CommonStep.ensureGameOpenAndInMain()
    CommonStep.into_jijian()
    base.randomClick(ui["jijian_{}_{}".format(0, 5)]["button"])
    time.sleep(base.sleep_time)
    if CommonStep.is_in_jijian_main():
        base.randomClick(ui["jijian_{}_{}".format(0, 5)]["button"])
        time.sleep(base.sleep_time)
    # 若线索交流开启中,则跳过任务
    if JiJianStep.isClueCommunicating():
        logger.info("线索交流开启中,跳过任务")
        return
    # 进入线索交流界面
    base.randomClick((460, 617, 480, 640))
    time.sleep(base.sleep_time)
    # 关闭线索交流结束界面
    if base.is_template_match("/jijian/clue_communicate_end.png"):
        base.randomClick((37, 30, 56, 48))
        time.sleep(base.sleep_time)
    img = base.screen(memery=True)
    JiJianStep.getClue()
    JiJianStep.receiveClue()
    # 判断1到7号线索是否已经放置
    num = 0
    map1 = {"1": (370, 222, 412, 255), "2": (557, 260, 608, 326), "3": (766, 180, 807, 230), "4": (988, 220, 1000, 268),
            "5": (645, 479, 688, 539), "6": (850, 431, 890, 472), "7": (414, 449, 459, 505)}
    for i in range(7):
        path = "/jijian/clue_{}.png".format(i + 1)
        if base.is_template_match(path, screen_re=img):
            logger.info("线索{}已经放置，跳过".format(i + 1))
            num += 1
            continue
        else:
            # 选择相应线索进入
            base.randomClick(map1[str(i + 1)])
            time.sleep(base.sleep_time)
            res = JiJianStep.anyClubCard()
            if len(res) == 0:
                base.randomClick((748, 564, 770, 600))
                time.sleep(base.sleep_time)
                continue
            elif len(res) == 5:
                x1, y1, x2, y2, s = res
                base.randomClick((x1, y1, x2, y2))
                num += 1
                time.sleep(base.sleep_time)
                # 退出选择相应线索
                base.randomClick((748, 564, 770, 600))
                time.sleep(base.sleep_time)
    # 判断能否解锁线索
    if num == 7:
        base.randomClick((633, 642, 693, 662))
        time.sleep(3 * base.sleep_time)
        # 重新进入线索交流界面
        base.randomClick((460, 617, 480, 640))
        time.sleep(base.sleep_time)
        num = 0
        for i in range(7):
            # 选择相应线索进入
            base.randomClick(map1[str(i + 1)])
            time.sleep(base.sleep_time)
            res = JiJianStep.anyClubCard()
            if len(res) == 0:
                base.randomClick((748, 564, 770, 600))
                time.sleep(base.sleep_time)
                continue
            elif len(res) == 5:
                x1, y1, x2, y2, s = res
                base.randomClick((x1, y1, x2, y2))
                num += 1
                time.sleep(base.sleep_time)
                # 退出选择相应线索
                base.randomClick((748, 564, 770, 600))
                time.sleep(base.sleep_time)
    JiJianStep.sendClue()
    CommonStep.ensureGameOpenAndInMain()


# 基建一键收货
@my_annotation(desc="基建一键收货")
@before
@func_set_timeout(base.timeout_time)
def jijian_receive():
    CommonStep.ensureGameOpenAndInMain()
    CommonStep.into_jijian()
    if JiJianStep.is_any_notification():
        JiJianStep.receive_notification()
    CommonStep.ensureGameOpenAndInMain()


# 基建使用无人机
@my_annotation(desc="基建使用无人机")
@before
@func_set_timeout(base.timeout_time)
def use_electricity():
    CommonStep.ensureGameOpenAndInMain()
    CommonStep.into_jijian()
    num = JiJianStep.now_electricity()
    if int(num[0]) < 20:
        return
    JiJianStep.use_electricity(base.get("a"), base.get("b"))
    CommonStep.ensureGameOpenAndInMain()


# 基建排班
@my_annotation(desc="基建排班")
@before
@func_set_timeout(base.timeout_time_max)
def schedual(path):
    msgList = []
    temp = base.read_json(base.project_path + path)
    back = copy.deepcopy(temp)
    schedual_dict = temp["Config"]
    data = schedual_dict["data"]
    CommonStep.ensureGameOpenAndInMain()
    CommonStep.into_jijian()
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
        msg = JiJianStep.do_schedual(x, y, names, type)
        msgList.append(msg)
        logger.info("安排：" + str(names) + " 入住：" + type + " ({},{})".format(x, y))
        # 修改index为下一位
        new_index = (index + 1) % num
        item["next_index"] = new_index
        logger.debug("set index:%s -> %s", index, new_index)
    base.write_json(temp, base.project_path + "/config/schedual.json")
    backpath = base.project_path + "/config/backup/"
    if not os.path.exists(backpath):
        os.makedirs(backpath)
    now = datetime.datetime.now()
    base.write_json(back, backpath + "schedual.json.{}.{}.{}.{}".format(now.month, now.day, now.hour, now.minute))
    sum = JiJianStep.auto_sleep()
    msgList.append("宿舍安排{}为干员进行休息".format(sum))
    base.send("排班完成", '\n'.join(msgList))
    base.state.is_scheduler = False
    CommonStep.ensureGameOpenAndInMain()


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
