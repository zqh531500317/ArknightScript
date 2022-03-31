from module.utils.core_picture import *
from module.utils.core_ocr import ocr_without_position, number_ocr
from module.utils.core_template import template_match_best, is_template_match
from logzero import logger
from datetime import datetime
from module.task.ziyuanshouji import findGame
from module.task.fight import fight
from module.inventory.demo import show_bag


def get_xinpian_info(xinpian_1, xinpian_2):
    randomClick("main_cangku")
    time.sleep(sleep_time)
    randomClick("cangku_yangcheng")
    time.sleep(sleep_time)
    scroll(1225, 475, 200, 475, 1000)
    scroll(1225, 475, 200, 475, 1000)
    scroll(1225, 475, 200, 475, 1000)
    xinpian_list = ["zz1", "zz2", "zz3", "fz1", "fz2", "fz3", "jj1", "jj2", "jj3",
                    "jw1", "jw2", "jw3", "ss1", "ss2", "ss3", "tz1", "tz2", "tz3",
                    "xf1", "xf2", "xf3", "zl1", "zl2", "zl3"]
    data = {}
    for i in range(1):
        screen_img = screen(memery=True)
        for item in xinpian_list:
            res = template_match_best("items/{}.png".format(item), screen_re=screen_img, template_threshold=0.9)
            if len(res) == 0:
                if not data.get(item):
                    data[item] = [0, 0.8, __get_map_name(item)]
                continue
            cropped = cut(screen_img, int(res[0]), int(res[3]), int(res[2]), int(res[3]) + 30)
            a = ocr_without_position(cropped, limit=number_ocr)[0]["words"]
            num = int(a)
            if not data.get(item):
                data[item] = [num, res[4], __get_map_name(item)]
            else:
                if data[item][1] < res[4]:
                    data[item] = [num, res[4], __get_map_name(item)]
        scroll(465, 475, 1240, 475, 3000)
    logger.debug("=======仓库芯片信息=======")
    for k, v in data.items():
        logger.debug("  %s  %s", k, str(v))
    res = __cal_by_data(data, xinpian_1, xinpian_2)
    logger.debug("=======缺少芯片信息=======")
    for k, v in res.items():
        logger.info("  %s  %s", k, str(v))
    return data, res


# res 缺少芯片信息
def do_xinpian(data, res):
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
        for k, v in res.items():
            game_name = v[1]
            if dayOfWeek not in openTime[game_name]:
                logger.info("目标:{},但是{}未开放，跳过".format(k, game_name))
                continue
            findGame(game_name)
            while True:
                if v[0] <= 0:
                    break
                fight(game_name, False, 0, False, 0)
                if not fightTime.get(game_name):
                    fightTime[game_name] = 1
                else:
                    fightTime[game_name] += 1
                logger.info("进行一场{},剩余芯片{}:{}".format(game_name, k, v[0]))
                screen_re = read(endFight_path)
                xinpian_list = ["zz1", "zz2", "fz1", "fz2", "jj1", "jj2",
                                "jw1", "jw2", "ss1", "ss2", "tz1", "tz2",
                                "xf1", "xf2", "zl1", "zl2"]
                name = None
                score = 0
                for i in xinpian_list:
                    b = template_match_best("items/s_{}.png".format(i), screen_re=screen_re, template_threshold=0.6)
                    if len(b) != 0:
                        if score < b[4]:
                            score = b[4]
                            name = i
                res[name][0] -= 1
                if not getTime.get(name):
                    getTime[name] = 0
                getTime[name] += 1
    except Exception as e:
        pass
    finally:
        logger.info("=======刷图情况=======")
        for k, v in fightTime.items():
            logger.info("%s %s", k, v)
        logger.info("=======芯片获取情况=======")
        for k, v in getTime.items():
            logger.info("%s %s", k, v)


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


def __get_map_name(item: str):
    return item.replace("3", "2").replace("1", "-1").replace("2", "-2").replace("zz", "PR-A").replace("zl",
                                                                                                      "PR-A").replace(
        "jj", "PR-B").replace("ss", "PR-B").replace("fz", "PR-C").replace("xf", "PR-C").replace("jw", "PR-D").replace(
        "tz", "PR-D")


def __cal_by_data(data: dict, limit1=6, limit2=10):
    res = {}
    for k, v in data.items():
        num = v[0]
        if k[2] == "3":
            num *= 2
            k = k[:2] + "2"
        if not res.get(k):
            res[k] = [num, v[2]]
        else:
            res[k][0] = res[k][0] + num
    for k in list(res.keys()):
        v = res[k]
        if k[2] == "1":
            if v[0] < limit1:
                v[0] = limit1 - v[0]
            else:
                del res[k]
        if k[2] == "2":
            if v[0] < limit2:
                v[0] = limit2 - v[0]
            else:
                del res[k]
    return res


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


if __name__ == '__main__':
    # get_xinpian_info(6, 10)
    __get_bag_info()
