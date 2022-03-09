import datetime
import module.step.click_step
import module.step.judge_step
import module.step.jijian_step
from module.utils.core_template import *

a = configList["Config"]["Game"]["a"]
b = configList["Config"]["Game"]["b"]


# 基建一键收货
@func_set_timeout(timeout_time)
def jijian_receive():
    module.step.judge_step.ensureGameOpenAndInMain()
    module.step.click_step.into_jijian()
    if module.step.jijian_step.is_any_notification():
        module.step.jijian_step.receive_notification()
    module.step.judge_step.ensureGameOpenAndInMain()


# 基建使用电力
@func_set_timeout(timeout_time)
def use_electricity():
    module.step.judge_step.ensureGameOpenAndInMain()
    module.step.click_step.into_jijian()
    num = module.step.jijian_step.now_electricity()
    if int(num[0]) < 20:
        return
    if module.step.jijian_step.is_any_notification():
        module.step.jijian_step.receive_notification()
        module.step.judge_step.ensureGameOpenAndInMain()
        module.step.click_step.into_jijian()
    module.step.jijian_step.use_electricity(a, b)
    module.step.judge_step.ensureGameOpenAndInMain()


# 基建排班
@func_set_timeout(timeout_time_max)
def schedual():
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
        if not get_interval(hour, minute):
            continue
        module.step.jijian_step.do_schedual(x, y, names, type)
        logger.info("安排：" + str(names) + " 入住：" + type + " ({},{})".format(x, y))
        # 修改index为下一位
        index = (index + 1) % num
        item["next_index"] = index
    cf.write_json(temp, project_path + "/config/schedual.json")
    module.step.jijian_step.auto_sleep()
    module.step.judge_step.ensureGameOpenAndInMain()


# 判断当前时间和排班时间是否在1h内，执行
def get_interval(hour1, minute1):
    hour = datetime.datetime.now().hour
    minute = datetime.datetime.now().minute
    if (hour1 == hour and minute >= minute1) or \
            (hour1 + 1 == hour and minute < minute1) \
            or (hour1 == 23 and hour == 0 and minute < minute1):
        flag = True
    else:
        flag = False
    return flag
