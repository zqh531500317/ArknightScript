import time

from module.utils.core_template import *
from module.utils.core_ocr import ocr_without_position
from module.error.ocr import CharactersNotFound
from cnstd import CnStd
from cnocr import CnOcr

cnstd = CnStd(rotated_bbox=False, resized_shape=(1280, 704))
ocr = CnOcr(model_name="densenet_lite_136-fc", cand_alphabet=cand_alphabet_officer)


def __pre_process(res):
    print(res)
    if res == "罗比拉塔":
        return "罗比菈塔"
    elif res == "桑赛":
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
    if not is_template_match("jijian/jinzhuxinxi.png"):
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
        click(965, 39)
        time.sleep(1)
        click(1045, 40)
        time.sleep(1)
        click(1045, 40)
    else:
        # 切换技能排序
        click(880, 40)
        time.sleep(1)
        click(965, 39)


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
def do_schedual(x, y, names, type):
    pre_schedual(x, y, type)
    screen()
    num = len(names)
    choosed_num = 0
    flag = False
    cyc_times = 5
    for index in range(cyc_times):
        screen()
        img = Image.open(screen_path)
        img = img.convert("RGBA")
        pixdata = img.load()
        for i in range(398):
            for j in range(720):
                pixdata[i, j] = (255, 255, 255, 255)
        for i in range(398, 1280):
            for j in range(720):
                if j < 321 or (348 < j < 603) or j > 629:
                    pixdata[i, j] = (255, 255, 255, 255)
        img.save(screen_path)
        img = Image.open(screen_path)
        box_infos = cnstd.detect(img)
        for box_info in box_infos['detected_texts']:
            box = box_info["box"]
            x = int((box[0] + box[2]) / 2)
            y = int((box[1] + box[3]) / 2)
            cropped_img = box_info['cropped_img']
            ocr_res = ocr.ocr_for_single_line(cropped_img)
            res = "".join(str(i) for i in ocr_res[0])
            res = __pre_process(res)
            if res in names:
                logger.info("选中干员%s", res)
                click(x, y)
                time.sleep(1)
                choosed_num += 1
                if choosed_num == num:
                    flag = True
                    break
        if flag:
            break
        scroll(1275, 350, 465, 350, 3000)
    later_schedual()


def auto_sleep():
    _auto_sleep = configList["Config"]["Game"]["auto_sleep"]
    if not _auto_sleep:
        return 0
    for ss in range(4):
        num = 5
        choosed_num = 0
        cyc_times = 5
        pre_schedual(ss + 1, 4, "宿舍")
        for index in range(cyc_times):
            working_dets = template_match_most("jijian/working.png")
            sleeping_dets = template_match_most("jijian/sleeping.png")
            emotion_dets = template_match_most("jijian/emotion.png")
            sleep_list = []
            for coord in emotion_dets:
                _cut = cut_by_path(screen_path, int(coord[0]),
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
                time.sleep(1)
                if choosed_num == num:
                    break
            if choosed_num == num:
                break
            scroll(1275, 350, 465, 350, 3000)
        later_schedual()
        if choosed_num < num:
            break


# 判断是否有收菜提示
def is_any_notification():
    b = compareSimilar("jijian_notification") > 0.75
    return b


# 进行收菜
def receive_notification():
    randomClick("jijian_notification")
    for i in range(5):
        time.sleep(2)
        randomClick((191, 658, 276, 705))


# 判断充能上限以及当前进度
# return [当前电力,总电力]
def now_electricity(index=3):
    screen()
    time.sleep(3)
    region = read(screen_path)
    cropped = cut(region, 762, 23, 862, 48)
    write(screen_path, cropped)
    time.sleep(5)
    result = ocr_without_position(screen_path)
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
    time.sleep(2)
    screen()
    res = template_match_most("jijian/trade_list.png", x1=0, x2=240)
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
        screen()
        img = Image.open(screen_path)
        img = img.convert("RGBA")
        pixdata = img.load()
        for i in range(398):
            for j in range(720):
                pixdata[i, j] = (255, 255, 255, 255)
        for i in range(700, 1280):
            for j in range(720):
                pixdata[i, j] = (255, 255, 255, 255)
        for i in range(554, 700):
            for j in range(580, 650):
                pixdata[i, j] = (255, 255, 255, 255)
        for i in range(398, 1280):
            for j in range(720):
                if j < 321 or (348 < j < 603) or j > 629:
                    pixdata[i, j] = (255, 255, 255, 255)
        img.save(screen_path)
        img = Image.open(screen_path)
        box_infos = cnstd.detect(img)
        for box_info in box_infos['detected_texts']:
            box = box_info["box"]
            x = int((box[0] + box[2]) / 2)
            y = int((box[1] + box[3]) / 2)
            cropped_img = box_info['cropped_img']
            ocr_res = ocr.ocr_for_single_line(cropped_img)
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


# 使用电力 a:第几行 b:第几列  example 1,1 表示电力使用与第一行第一列的建筑
def use_electricity(a, b):
    efficient = configList["Config"]["Game"]["efficient"]
    if efficient:
        if special_electricity():
            return
    else:
        randomClick(ui["jijian_{}_{}".format(a, b)]["button"])
        time.sleep(3)
    # 点击经验书或赤金
    randomClick((41, 570, 124, 650))
    time.sleep(2)
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
    time.sleep(2)
    randomClick((1210, 530, 1234, 547))
    time.sleep(2)
    # 点击最多
    randomClick((934, 319, 989, 353))
    time.sleep(2)
    # 点击确定
    randomClick((837, 565, 1000, 600))
    time.sleep(3)
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
        time.sleep(3)
        # 点击最多
        randomClick((934, 319, 989, 353))
        time.sleep(2)
        # 点击确定
        randomClick((837, 565, 1000, 600))
        time.sleep(3)
        res = template_match_best("jijian/trade_deliverable.png")
        if len(res) == 0:
            break
        randomClick((res[0], res[1], res[2], res[3]))
        time.sleep(3)


def is_in_jijian_main():
    return is_template_match("jijian/jijian_main.png")
