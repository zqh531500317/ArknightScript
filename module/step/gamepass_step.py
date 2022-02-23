import module.error.game
from retrying import retry
import math
from module.utils.core_template import *
from module.utils.core_ocr import ocr_with_position
from module.utils.core_clickLoader import dic

def exec_by_clickLoader(v):
    for i, action in enumerate(v):
        time.sleep(5)
        if action[0] == "click":
            randomClick(action[1])
        elif action[0] == "scroll":
            scroll_by_tuple(action[1])


# 为主线 滑动到最左边
def goto_ahead_for_zhuxian():
    for i in range(5):
        scroll(520, 40, 1400, 43, 150)
        time.sleep(3)


# 为活动 滑动到最左边
def goto_ahead_for_huodong():
    for i in range(3):
        scroll(520, 40, 1400, 43, 150)
        time.sleep(3)


# 为资源本 滑动到最左边
def goto_ahead_for_ziyuanshouji():
    scroll(200, 300, 1000, 300, 150)
    time.sleep(2)
    scroll(200, 300, 1000, 300, 150)


# 为资源本 滑动到最右边
def goto_behind_for_ziyuanshouji():
    scroll(1000, 300, 200, 300, 150)
    time.sleep(2)
    scroll(1000, 300, 200, 300, 150)


# 判断剿灭是否打完 return num 表示还要打num把才能打完
def jiaomieIsFinish():
    time.sleep(2)
    screen()
    time.sleep(3)
    region = read(screen_path)
    cropped = cut(region, 585, 193, 687, 225)
    write(screen_path, cropped)
    time.sleep(3)
    result = ocr_with_position(screen_path)
    print(result)
    x = result[len(result) - 1]["words"]
    if x[0] == "/":
        now = 0
    else:
        now = int(x)
    temp = num = (1800 - now) / 360
    while True:
        if 0 <= temp <= 1:
            break
        temp = temp - 1
    if temp < 0.9:
        re = math.floor(num)
    else:
        re = math.ceil(num)
    logger.info("当前剿灭进度为：%s,即将进行最多%s次剿灭作战", now, re)
    return re


# 利用ocr寻找关卡位置
@retry(stop_max_attempt_number=2)
def find_game_position(name, type="zhuxian"):
    temp = []
    # 随机点击关卡的位置区域
    x1 = 0
    x2 = 0
    y1 = 0
    y2 = 0

    if type == "ziyuanshouji":
        # 解析game内容
        left = name[:2]
        right = name[3]
        if left == "PR":
            left = left + right
        ch_names = dic[left]

        screen()
        list = ocr_with_position(project_path + "/cache/screen.png")
        for one in list:
            for ch_name in ch_names:
                if one["words"].lower() == ch_name.lower():
                    logger.info("识别到关卡%s", name)
                    flag = 1
                    location = one["location"]
                    x1 = location["left"]
                    y1 = location["top"]
                    x2 = x1 + location["width"]
                    y2 = y1 + location["height"]
                    randomClick((x1, y1, x2, y2))
                    return

        logger.error("未找到关卡%s", name)
        raise module.error.game.GameNotFound(name)
        # 是否找到位置  0暂时未找到 1找到 -1找不到
    if type == "zhuxian" or type == "huodong":
        flag = 0
        while True:
            logger.info("尝试寻找关卡%s", name)
            screen()
            list = ocr_with_position(project_path + "/cache/screen.png")
            if temp == list:
                flag = -1
                break
            for one in list:
                if one["words"].lower() == name.lower():
                    logger.info("识别到关卡%s", name)
                    flag = 1
                    location = one["location"]
                    x1 = location["left"]
                    y1 = location["top"]
                    x2 = x1 + location["width"]
                    y2 = y1 + location["height"]
                    break
            if flag == 1:
                break
            temp = list
            scroll(1000, 40, 760, 43, 200)
            time.sleep(3)

        if flag == -1:
            logger.error("未找到关卡%s", name)
            for i in range(6):
                scroll(600, 40, 1000, 43, 200)
                time.sleep(2)

            raise module.error.game.GameNotFound(name)
        randomClick((x1, y1, x2, y2))


# 利用模板匹配寻找关卡位置
@retry(stop_max_attempt_number=2)
def find_game_position_with_template(name, type="zhuxian"):
    # 随机点击关卡的位置区域
    x1 = 0
    x2 = 0
    y1 = 0
    y2 = 0

    if type == "zhuxian" or type == "huodong":
        flag = 0
        times = 0
        while True:
            logger.info("尝试寻找关卡%s", name)
            screen()
            det = template_match_best("/map/" + name + ".png")
            if len(det) == 0:
                continue
            if det[4] > 0.95:
                logger.info("识别到关卡%s", name)
                flag = 1
                x1 = det[0]
                y1 = det[1]
                x2 = det[2]
                y2 = det[3]
            if flag == 1:
                break
            scroll(1000, 40, 760, 43, 200)
            time.sleep(3)
            if times > 20:
                flag = -1
                break
            times = times + 1
    if flag == -1:
        logger.error("未找到关卡%s", name)
        for i in range(6):
            scroll(600, 40, 1000, 43, 200)
            time.sleep(2)

        raise module.error.game.GameNotFound(name)
    randomClick((x1, y1, x2, y2))
