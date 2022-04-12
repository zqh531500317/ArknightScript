import time

from module.utils.core_picture import *
from module.utils.core_template import *
from module.utils.core_ocr import ocr_without_position, jijian_ocr, cnstd, number_ocr
from module.error.ocr import CharactersNotFound
from module.utils.core_email import send
from module.utils.core_control import *
import module.step.judge_step
import module.step.click_step
from module.utils.core_log import OcrLogger

ocr_logger = OcrLogger.ocr_logger


def __pre_process(res):
    ocr_logger.info(res)
    if res == "罗比拉塔":
        return "罗比菈塔"
    elif res == "桑赛" or res == "桑进":
        return "桑葚"
    else:
        return res


def pre_schedual(x, y, type):
    # 进入建筑
    randomClick(ui["jijian_{}_{}".format(x, y)]["button"])
    time.sleep(sleep_time)
    if is_in_jijian_main():
        randomClick(ui["jijian_{}_{}".format(x, y)]["button"])
        time.sleep(sleep_time)
    # 点击 进驻信息  入住
    if not is_template_match("/jijian/qingkong.png", template_threshold=0.9):
        logger.debug("点击 进驻信息 入住")
        randomClick((40, 273, 70, 315))
        time.sleep(sleep_time)
    # 清空选择
    randomClick((1175, 20, 1221, 42))
    time.sleep(sleep_time)
    if is_template_match("jijian/ensure_clear.png"):
        click(838, 494)
        time.sleep(sleep_time * 3)
    # 进入选择干员界面
    randomClick((937, 149, 1060, 184))
    time.sleep(sleep_time)

    if type == "宿舍":
        # 切换心情排序
        click(670, 39)
        time.sleep(1)
        click(974, 40)
        time.sleep(1)
        click(974, 40)
    else:
        # 切换技能排序
        click(974, 40)
        time.sleep(1)
        click(885, 39)
    time.sleep(sleep_time)


def later_schedual():
    # 点击确定
    randomClick((1155, 670, 1200, 689))
    time.sleep(sleep_time)
    if is_template_match("jijian/comfirm_schedule.png"):
        randomClick((888, 670, 950, 699))
        time.sleep(sleep_time)
    # 退出到基建首页
    click(43, 40)
    time.sleep(sleep_time)


# names干员名称 type设施名称
def do_schedual(x1, y1, names, type, retry_time=0):
    pre_schedual(x1, y1, type)
    num = len(names)
    choosed_num = 0
    flag = False
    cyc_times = 5
    temp = []
    for index in range(cyc_times):
        img = screen(memery=True)
        for i in range(398):
            for j in range(720):
                img[j, i] = (255, 255, 255)
        for i in range(398, 1280):
            for j in range(720):
                if j < 321 or (348 < j < 603) or j > 629:
                    img[j, i] = (255, 255, 255)
        save2("test", img)
        box_infos = cnstd.detect(img)
        for box_info in box_infos['detected_texts']:
            box = box_info["box"]
            x = int((box[0] + box[2]) / 2)
            y = int((box[1] + box[3]) / 2)
            cropped_img = box_info['cropped_img']
            ocr_res = jijian_ocr.ocr_for_single_line(cropped_img)
            res = "".join(str(i) for i in ocr_res[0])
            res = __pre_process(res)
            if res in names:
                temp.append(res)
                click(x, y)
                time.sleep(1)
                choosed_num += 1
                if choosed_num == num:
                    flag = True
                    break
        if flag:
            break
        scroll(1275, 350, 465, 350, 3000)
    msg = "x={},y={},name={},type={},选中干员={}".format(x1, y1, names, type, str(temp))
    logger.info(msg)
    later_schedual()
    if choosed_num < num and type != "宿舍":
        retry_time += 1
        if retry_time == 3:
            logger.error("排班可能出错%s,已重试次数%s", msg, retry_time)
            send("排班可能出错", msg)
            return msg
        else:
            logger.warning("换班异常,{%s},重新尝试第%s次", msg, retry_time)
            module.step.judge_step.ensureGameOpenAndInMain()
            module.step.click_step.into_jijian()
            return do_schedual(x1, y1, names, type, retry_time)
    return msg


# 判断是否有收菜提示
def is_any_notification():
    b = compareSimilar("jijian_notification") > 0.75
    return b


# 进行收菜
def receive_notification():
    randomClick("jijian_notification")
    for i in range(5):
        time.sleep(sleep_time)
        randomClick((191, 658, 276, 705))


# 判断充能上限以及当前进度
# return [当前电力,总电力]
def now_electricity(index=3):
    region = screen(memery=True)
    cropped = cut(region, 762, 23, 862, 48)
    result = ocr_without_position(cropped, number_ocr)
    print(result)
    num = []
    try:
        num = result[0]["words"].split("/")
    except CharactersNotFound as e:
        if index > 0:
            e.message(index)
            index = index - 1
            now_electricity(index)

    return num


def special_electricity():
    res = template_match_best("jijian/trade.png")
    randomClick((
        int(res[0]),
        int(res[1])
        , int(res[2])
        , int(res[3])
    ))
    time.sleep(sleep_time)
    if is_in_jijian_main():
        randomClick((
            int(res[0]),
            int(res[1])
            , int(res[2])
            , int(res[3])
        ))
        time.sleep(sleep_time)
    # 点击经验书或赤金
    randomClick((41, 570, 124, 650))
    time.sleep(sleep_time)
    screen_re = screen(memery=True)[0: 720, 0: 240]
    res = template_match_most("jijian/trade_list.png", screen_re=screen_re)
    for item in res:
        randomClick((
            int(item[0]),
            int(item[1])
            , int(item[2])
            , int(item[3])
        ))
        time.sleep(sleep_time)
        randomClick((395, 625, 460, 653))
        time.sleep(sleep_time)
        img = screen(memery=True)
        for i in range(398):
            for j in range(720):
                img[j, i] = (255, 255, 255)
        for i in range(700, 1280):
            for j in range(720):
                img[j, i] = (255, 255, 255)
        for i in range(554, 700):
            for j in range(580, 650):
                img[j, i] = (255, 255, 255)
        for i in range(398, 1280):
            for j in range(720):
                if j < 321 or (348 < j < 603) or j > 629:
                    img[j, i] = (255, 255, 255)
        box_infos = cnstd.detect(img)
        for box_info in box_infos['detected_texts']:
            box = box_info["box"]
            x = int((box[0] + box[2]) / 2)
            y = int((box[1] + box[3]) / 2)
            cropped_img = box_info['cropped_img']
            ocr_res = jijian_ocr.ocr_for_single_line(cropped_img)
            res = "".join(str(i) for i in ocr_res[0])
            res = __pre_process(res)
            if "巫恋" == res:
                click(41, 39)
                time.sleep(sleep_time)
                use_electricity_trade(1)
                return True
        click(41, 39)
        time.sleep(sleep_time)
    click(41, 39)
    time.sleep(sleep_time)
    click(41, 39)
    time.sleep(sleep_time)
    return False


# 使用电力 a:第几行 b:第几列  example 1,1 表示电力使用与第一行第一列的建筑
def use_electricity(a, b):
    if cf.configList["Config"]["Game"]["efficient"]:
        if special_electricity():
            return
    randomClick(ui["jijian_{}_{}".format(a, b)]["button"])
    time.sleep(sleep_time)
    if is_in_jijian_main():
        randomClick(ui["jijian_{}_{}".format(a, b)]["button"])
        time.sleep(sleep_time)
    # 点击经验书或赤金
    randomClick((41, 570, 124, 650))
    time.sleep(sleep_time)
    # 判断加速类型
    if is_template_match("jijian/manufacturing_experience_book.png"):
        use_electricity_manufacturing(1)
    elif is_template_match("jijian/manufacturing_gold_bar.png"):
        use_electricity_manufacturing(2)
    elif is_template_match("jijian/manufacturing_jade.png"):
        use_electricity_manufacturing(3)
    elif is_template_match("jijian/trade_money.png"):
        use_electricity_trade(1)
    elif is_template_match("jijian/trade_jade.png"):
        use_electricity_trade(2)


# 1经验书 2赤金 3原石碎片
def use_electricity_manufacturing(kind):
    # 点击快进符号
    time.sleep(sleep_time)
    randomClick((1210, 530, 1234, 547))
    time.sleep(sleep_time)
    # 点击最多
    randomClick((934, 319, 989, 353))
    time.sleep(sleep_time)
    # 点击确定
    randomClick((837, 565, 1000, 600))
    time.sleep(sleep_time)
    # 点击任意位置
    randomClick((994, 66, 1144, 138))
    # 点击收取
    randomClick((1080, 618, 1186, 667))


# 1龙门币 2合成玉
def use_electricity_trade(kind):
    while True:
        res = template_match_best("jijian/trade_faster.png")
        if len(res) == 0:
            return
        randomClick((res[0], res[1], res[2], res[3]))
        time.sleep(sleep_time)
        # 点击最多
        randomClick((934, 319, 989, 353))
        time.sleep(sleep_time)
        # 点击确定
        randomClick((837, 565, 1000, 600))
        time.sleep(sleep_time)
        res = template_match_best("jijian/trade_deliverable.png")
        if len(res) == 0:
            break
        randomClick((res[0], res[1], res[2], res[3]))
        time.sleep(sleep_time)


def is_in_jijian_main():
    return is_template_match("jijian/jijian_main.png")


def auto_sleep():
    sum = 0
    _auto_sleep = configList["Config"]["Game"]["auto_sleep"]
    if not _auto_sleep:
        return 0
    for ss in range(4):
        num = 5
        choosed_num = 0
        cyc_times = 5
        pre_schedual(ss + 1, 4, "宿舍")
        for index in range(cyc_times):
            screen_re = screen(memery=True)
            working_dets = template_match_most("jijian/working.png", screen_re=screen_re)
            sleeping_dets = template_match_most("jijian/sleeping.png", screen_re=screen_re)
            emotion_dets = template_match_most("jijian/emotion.png", screen_re=screen_re)
            sleep_list = []
            for coord in emotion_dets:
                _cut = cut(screen_re, int(coord[0]),
                           int(coord[1]),
                           int(coord[2]),
                           int(coord[3]))
                flag = False
                for y in range(_cut.shape[0]):
                    if flag:
                        break
                    for x in range(_cut.shape[1]):
                        rgb = _cut[y, x]
                        if (130 <= rgb[2] <= 150) and (190 <= rgb[1] <= 210) and (60 <= rgb[0] <= 70):
                            flag = True
                            break
                if not flag:
                    sleep_list.append([int(coord[0]),
                                       int(coord[1]),
                                       int(coord[2]),
                                       int(coord[3])])
            for i in range(len(sleep_list) - 1, -1, -1):
                flag = False
                pos_x = sleep_list[i][2] + 10
                pos_y = sleep_list[i][1] - 72
                for coord in working_dets:
                    if int(coord[0]) <= pos_x <= int(coord[2]) and \
                            int(coord[1]) <= pos_y <= int(coord[3]):
                        flag = True
                        break
                if not flag:
                    for coord in sleeping_dets:
                        if int(coord[0]) <= pos_x <= int(coord[2]) and \
                                int(coord[1]) <= pos_y <= int(coord[3]):
                            flag = True
                            break
                if flag:
                    sleep_list.remove(sleep_list[i])
            for item in sleep_list:
                randomClick((item[0], item[1], item[2], item[3]))
                choosed_num += 1
                sum += 1
                time.sleep(1)
                if choosed_num == num:
                    break
            if choosed_num == num:
                break
            scroll(1275, 350, 465, 350, 3000)
        later_schedual()
        if choosed_num < num:
            break
    return sum


def isClueCommunicating():
    return is_template_match("/jijian/clue_communicate.png")


def anyClubCard():
    return template_match_best('/jijian/clue_any_card.png')


# 接收线索
def getClue():
    # into
    randomClick((1186, 170, 1216, 190))
    time.sleep(2 * sleep_time)
    # 全部收取
    randomClick((770, 570, 850, 580))
    time.sleep(3 * sleep_time)
    # quit
    randomClick((980, 94, 1000, 110))
    time.sleep(sleep_time)


# 接收线索
def receiveClue():
    # into
    randomClick((1186, 270, 1216, 290))
    time.sleep(2 * sleep_time)
    # 全部收取
    randomClick((1000, 670, 1100, 700))
    time.sleep(3 * sleep_time)
    # quit
    randomClick((700, 570, 750, 590))
    time.sleep(sleep_time)


# 传递线索
def sendClue():
    # into
    randomClick((1186, 371, 1216, 400))
    time.sleep(2 * sleep_time)
    while True:
        res = anyClubCard()
        if len(res) == 0:
            break
        x1, y1, x2, y2, s = res
        randomClick((x1, y1, x2, y2))
        time.sleep(1)
        randomClick((1185, 117, 1201, 151))
        time.sleep(sleep_time)
    # quit sendClue
    click(1244, 35)
    time.sleep(2 * sleep_time)


if __name__ == '__main__':
    do_schedual(2, 5, ["sadsad"], "办公室")
