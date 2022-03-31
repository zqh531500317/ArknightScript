import copy

from module.utils.core_picture import *
from module.utils.core_ocr import ocr_without_position, number_ocr
from module.utils.core_template import template_match_best, is_template_match
from logzero import logger
from datetime import datetime
from module.task.ziyuanshouji import findGame
from module.task.fight import fight
from module.inventory.demo import show_bag
from module.penguin_stats.core import analyse, get_name_by_id


def receive_daily_renwu():
    if compareSimilar("daily_renwu") >= 0.9:
        randomClick("daily_renwu")
        time.sleep(sleep_time)
        randomClick("renwu_receive")
        time.sleep(sleep_time)
        click(638, 645)


def receive_weekly_renwu():
    if compareSimilar("weekly_renwu") >= 0.9:
        randomClick("weekly_renwu")
        time.sleep(sleep_time)
        randomClick("renwu_receive")
        time.sleep(sleep_time)
        click(638, 645)


def friend_home():
    time.sleep(2 * sleep_time)
    screen()
    region = read(screen_path)
    cropped = cut(region, 1187, 28, 1277, 52)
    write(screen_path, cropped)
    time.sleep(2 * sleep_time)
    result = ocr_without_position(screen_path, number_ocr)
    pre = result[0]["words"]
    while True:
        randomClick("friend_home")
        time.sleep(3 * sleep_time)
        screen()
        region = read(screen_path)
        cropped = cut(region, 1187, 28, 1277, 52)
        write(screen_path, cropped)
        result = ocr_without_position(screen_path)
        later = result[0]["words"]
        if pre == later:
            return
        pre = later


def __get_map_name(name: str):
    head = name[:2]
    if head == "近卫":
        head = "PR-D"
    elif head == "医疗":
        head = "PR-A"
    elif head == "狙击":
        head = "PR-B"
    elif head == "术师":
        head = "PR-B"
    elif head == "辅助":
        head = "PR-C"
    elif head == "先锋":
        head = "PR-C"
    elif head == "特种":
        head = "PR-D"
    elif head == "重装":
        head = "PR-A"
    else:
        return None
    if len(name) == 4:
        later = "-1"
    elif len(name) == 5:
        later = "-2"
    else:
        return None
    return head + later


def __cal_by_data(data: dict, limit1=6, limit2=10):
    res = {}
    temp = {}
    for k, v in data.items():
        if k[2] == "双":
            name = k[:2] + "芯片组"
            num = v["num"] * 2
            temp[name] = num
        else:
            res[k] = v
    for k, v in temp.items():
        if k not in res:
            map_name = __get_map_name(k)
            res[k] = {"num": v, "map_name": map_name}
        else:
            res[k]["num"] = res[k]["num"] + v
    for k, v in res.items():
        if len(k) == 4:
            v["num"] = limit1 - v["num"]
        elif len(k) == 5:
            v["num"] = limit2 - v["num"]
    res1 = {}
    for k, v in res.items():
        if v["num"] > 0:
            res1[k] = v
    return res1


def get_xinpian_info(xinpian_1=6, xinpian_2=10):
    randomClick("main_cangku")
    time.sleep(sleep_time)
    bag_info = __get_bag_info()
    xinpian_info = {}
    for name, v in bag_info.items():
        num = v["num"]
        map_name = __get_map_name(name)
        if map_name is None:
            continue
        xinpian_info[name] = {"num": num, "map_name": map_name}
    logger.debug("精二芯片每种目标数量:%s 精一芯片每种目标数量:%s", xinpian_2, xinpian_2)
    logger.debug("=======仓库芯片信息=======")
    for k, v in xinpian_info.items():
        logger.debug("  %s  %s", k, str(v))
    queshao_info = __cal_by_data(copy.deepcopy(xinpian_info), xinpian_1, xinpian_2)

    logger.debug("=======缺少芯片信息=======")
    for k, v in queshao_info.items():
        logger.info("  %s  %s", k, str(v))
    return xinpian_info, queshao_info


def __get_bag_info():
    bag_info = {}
    pre_items = None
    while True:
        items = show_bag()
        later_items = items.keys()
        if pre_items == later_items:
            break
        bag_info.update(items)
        scroll(1240, 475, 465, 475, 3000)
        pre_items = later_items
    return bag_info


# res 缺少芯片信息
def do_xinpian(xinpian_info, queshao_info):
    dayOfWeek = datetime.now().isoweekday()
    hour = datetime.now().hour
    if 0 <= hour <= 3:
        if dayOfWeek == 1:
            dayOfWeek = 7
        else:
            dayOfWeek -= 1
    logger.info("当前为星期%s", dayOfWeek)
    # 关卡开放信息
    openTime = {}
    # 作战信息
    fightTime = {}
    # 芯片获取信息
    getTime = {}
    openTime["PR-A-1"] = [1, 4, 5, 7]
    openTime["PR-A-2"] = [1, 4, 5, 7]
    openTime["PR-C-1"] = [3, 4, 6, 7]
    openTime["PR-C-2"] = [3, 4, 6, 7]
    openTime["PR-B-1"] = [1, 2, 5, 6]
    openTime["PR-B-2"] = [1, 2, 5, 6]
    openTime["PR-D-1"] = [2, 3, 6, 7]
    openTime["PR-D-2"] = [2, 3, 6, 7]
    try:
        for k, v in queshao_info.items():
            game_name = v["map_name"]
            if dayOfWeek not in openTime[game_name]:
                logger.info("目标:{},但是{}未开放，跳过".format(k, game_name))
                continue
            findGame(game_name)
            while True:
                if v["num"] <= 0:
                    break
                fight(game_name, False, 0, False, 0)
                if not fightTime.get(game_name):
                    fightTime[game_name] = 1
                else:
                    fightTime[game_name] += 1
                logger.info("进行一场{}".format(game_name))
                data, display = analyse()
                drop_name = ""
                for drop in data["drops"]:
                    drop_id = drop["itemId"]
                    if drop_id in ["3211", "3212", "3213",
                                   "3221", "3222", "3223",
                                   "3231", "3232", "3233",
                                   "3241", "3242", "3243",
                                   "3251", "3252", "3253",
                                   "3261", "3262", "3263",
                                   "3271", "3272", "3273",
                                   "3281", "3282", "3283"]:
                        drop_name = get_name_by_id(drop_id)
                        break
                queshao_info[drop_name]['num'] -= 1
                if not getTime.get(drop_name):
                    getTime[drop_name] = 0
                getTime[drop_name] += 1
    except Exception as e:
        pass
    finally:
        logger.info("=======刷图情况=======")
        for k, v in fightTime.items():
            logger.info("%s %s", k, v)
        logger.info("=======芯片获取情况=======")
        for k, v in getTime.items():
            logger.info("%s %s", k, v)


if __name__ == '__main__':
    # get_xinpian_info(6, 10)
    # __get_bag_info()
    get_xinpian_info()
