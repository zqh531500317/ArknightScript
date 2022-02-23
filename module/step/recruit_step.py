import itertools

from module.utils.core_picture import *
from module.utils.core_ocr import ocr_with_position,ocr_without_position,recruit_ocr
from module.utils.core_email import send
import module.utils.core_recruitLoader

recruit_tag = ui["recruit_tag"]["area"]


def recruit():
    state = get_state()
    if state == "waiting":
        logger.info("公开招募1号位正在招募中，跳过本次任务")
        return
    if state == "finish":
        randomClick("recruit_state_finish")
        time.sleep(5)
        randomClick("recruit_finish_skip")
        time.sleep(3)
        screen()
        save1("recruit", "result")
        randomClick("recruit_finish_skip")
        time.sleep(2)
        state = "empty"
    if state == "empty":
        randomClick("recruit_state_empty")
        time.sleep(2)
        while True:
            r = best_choose()
            if r == -1:
                return
            if r == 999:
                save1("recruit", "tags")
                return
            elif r == 1:
                save1("recruit", "tags")
                randomClick("recruit_do")
                return
            elif r == 0:
                b = is_flashable()
                if not b:
                    save1("recruit", "tags")
                    randomClick("recruit_do")
                    return
                elif b:
                    randomClick("recruit_flash")
                    time.sleep(2)
                    randomClick("recruit_flash_ensure")
                    time.sleep(2)


def is_flashable():
    screen()
    time.sleep(2)
    rgb = getRGB(970, 408)
    if rgb[0] == 0 and rgb[1] == 152 and rgb[2] == 220:
        return True
    return False


def get_state():
    if compareSimilar("recruit_state_waiting") > 0.85:
        return "waiting"
    elif compareSimilar("recruit_state_empty") > 0.75:
        return "empty"
    elif compareSimilar("recruit_state_finish") > 0.85:
        return "finish"


def get_recruit_num():
    screen()
    time.sleep(2)
    region = read(screen_path)
    x1 = 848
    y1 = 27
    x2 = 906
    y2 = 53
    cropped = cut(region, x1, y1, x2, y2)
    write(screen_path, cropped)
    time.sleep(3)
    result = ocr_without_position(screen_path)
    num = result[0]["words"]
    logger.debug("招聘许可数量：" + num)
    return int(num)


# return 999：高姿、资深   1：4星以上或支援机械  0：无特殊tag -1 error
def best_choose():
    result = _recruit_result1()
    template = module.utils.core_recruitLoader.recruit
    str = _ensure_ocr_correct(result)
    if str is not None:
        send("公开招募识别出错", str)
        return -1
    for item in result:
        tag = item["words"]
        if "flag" in item:
            x1 = item["location"]["x1"]
            y1 = item["location"]["y1"]
            x2 = item["location"]["x2"]
            y2 = item["location"]["y2"]
        else:
            x1 = recruit_tag[0] + item["location"]["left"]
            y1 = recruit_tag[1] + item["location"]["top"]
            x2 = item["location"]["width"] + x1
            y2 = item["location"]["height"] + y1
        if tag == "高级资深干员" or len(tag) >= 5 or tag == "资深干员":
            logger.info("出现资深干员词条，尝试发送邮件")
            msg = "公招词条内容为:"
            for i in result:
                tag = i["words"]
                msg = msg + tag + " "
            send("公开招募出资深了！！", msg)
            return 999
        if tag == "支援机械":
            _switch_time("min")
            randomClick((x1, y1, x2, y2))
            logger.info("有支援机械tag,已选择时间至1小时")
            return 1
    match_list = _all_match(result, template)
    _switch_time("max")
    str = ""
    if match_list[0][1][1] >= 3:
        combination = match_list[0][1][3][0][0]
        template_item = match_list[0][1][3][0][1]
        for n in combination:
            if n["words"] in template_item[2]:
                if "flag" in n:
                    x1 = n["location"]["x1"]
                    y1 = n["location"]["y1"]
                    x2 = n["location"]["x2"]
                    y2 = n["location"]["y2"]
                else:
                    x1 = recruit_tag[0] + n["location"]["left"]
                    y1 = recruit_tag[1] + n["location"]["top"]
                    x2 = n["location"]["width"] + x1
                    y2 = n["location"]["height"] + y1
                randomClick((x1, y1, x2, y2))
                str = str + n["words"] + " "
                time.sleep(2)

        logger.info("选中干员%s————tag组合为%s", template_item[0], str)
        return 1
    else:
        logger.info("未有4星及以上的tag组合,已选择时间至9小时")
        return 0


def _recruit_result():
    screen()
    time.sleep(3)
    region = read(screen_path)
    x1 = recruit_tag[0]
    y1 = recruit_tag[1]
    x2 = recruit_tag[2]
    y2 = recruit_tag[3]
    cropped = cut(region, x1, y1, x2, y2)
    write(screen_path, cropped)
    time.sleep(3)
    result = ocr_with_position(screen_path)
    logger.debug("词条内容是：" + str(result))
    return result


# 对于不能识别文字位置的cnocr 进行不同处理，用flag=1标志
def _recruit_result1():
    area = [
        (375, 371, 519, 396),
        (544, 371, 683, 396),
        (711, 371, 851, 396),
        (375, 442, 519, 467),
        (544, 442, 683, 467),
    ]
    result = []
    screen()
    r = cv2.imread(screen_path, 1)
    for i in range(5):
        a = area[i]
        s = cut(r, a[0], a[1], a[2], a[3])
        write(screen_path, s)
        res = ocr_without_position(screen_path, recruit_ocr)
        result.append({'flag': 1, 'words': res[0]["words"], 'location':
            {'x1': a[0], 'y1': a[1], 'x2': a[2], 'y2': a[3]}})
    logger.debug("词条内容是：" + str(result))
    return result


def _switch_time(mode):
    hour_high = (424, 136, 485, 164)
    hour_low = (417, 283, 483, 311)
    minute_high = (586, 136, 651, 164)
    minute_low = (586, 283, 651, 311)
    if mode == "max":
        randomClick(hour_low)
    elif mode == "min":
        pass


def _ensure_ocr_correct(recruit_result):
    for n in recruit_result:
        if not n["words"] in module.utils.core_recruitLoader.tags:
            return n["words"]
    return None


def _get_combinations(items):
    res = []
    for i in range(1, 4):
        iter = itertools.combinations(items, i)
        res = res + list(iter)
    return res


def _get_simple_ocr_item(ocr_items):
    simple_ocr_item = []
    for n in ocr_items:
        simple_ocr_item.append(n["words"])
    simple_ocr_item.sort()
    return tuple(simple_ocr_item)


def _all_match(ocr_items, template):
    match_dict = {}
    combinations = _get_combinations(ocr_items)
    for n in combinations:
        for m in template:
            simple_ocr_item = _get_simple_ocr_item(n)
            hashv = hash(str(simple_ocr_item))
            if m[1] != 5 and m[1] >= 2:
                if set(simple_ocr_item) <= set(m[2]):
                    star = m[1]
                    if hashv not in match_dict:
                        match_dict[hashv] = [simple_ocr_item, star, 0, [(n, m)]]
                    else:
                        if star < match_dict[hashv][1]:
                            match_dict[hashv][1] = star
                        match_dict[hashv][3].append((n, m))
    for k, v in match_dict.items():
        v[2] = len(v[3])
    match_list = sorted(match_dict.items(), key=lambda x: x[1][1], reverse=True)
    return match_list
