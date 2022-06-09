from retrying import retry

import module.error.game
from module.base import *
from module.stage import recognize_all_screen_stage_tags
from module.utils.core_clickLoader import dic


class GamePassStep:
    # 获取当前的关卡信息
    @staticmethod
    def stage():
        data = recognize_all_screen_stage_tags(base.screen(memery=True))
        return data

    @staticmethod
    def exec_by_clickLoader(v):
        time.sleep(base.sleep_time)
        for i, action in enumerate(v):
            if action[0] == "click":
                base.randomClick(action[1])
            elif action[0] == "scroll":
                base.scroll_by_tuple(action[1])
            time.sleep(base.THREE_MINUTES)

    # 为主线 滑动到最左边
    @staticmethod
    def goto_ahead_for_zhuxian():
        for i in range(5):
            base.scroll(520, 40, 1400, 43, 150)
            time.sleep(base.ONE_MINUTES)

    # 为活动 滑动到最左边
    @staticmethod
    def goto_ahead_for_huodong():
        for i in range(3):
            base.scroll(520, 40, 1400, 43, 150)
            time.sleep(base.ONE_MINUTES)

    # 为资源本 滑动到最左边
    @staticmethod
    def goto_ahead_for_ziyuanshouji():
        base.scroll(200, 300, 1000, 300, 150)
        time.sleep(base.ONE_MINUTES)
        base.scroll(200, 300, 1000, 300, 150)

    # 为资源本 滑动到最右边
    @staticmethod
    def goto_behind_for_ziyuanshouji():
        base.scroll(1000, 300, 200, 300, 150)
        time.sleep(base.ONE_MINUTES)
        base.scroll(1000, 300, 200, 300, 150)

    @staticmethod
    def goto_behind_for_huodong():
        base.scroll(1000, 300, 200, 300, 150)
        time.sleep(base.ONE_MINUTES)
        base.scroll(1000, 300, 200, 300, 150)
        time.sleep(base.ONE_MINUTES)
        base.scroll(1000, 300, 200, 300, 150)
        time.sleep(base.ONE_MINUTES)

    # 判断剿灭是否打完 return num 表示还要打num把才能打完
    @staticmethod
    def jiaomieIsFinish():
        time.sleep(base.sleep_time)
        region = base.screen(memery=True)
        cropped = base.cut(region, 104, 640, 279, 675)
        result = base.ocr_without_position(cropped, limit=None, cand_alphabet="1234567890/")
        x = result[len(result) - 1]["words"]
        if x[0] == "/":
            now = 0
        elif '/' in x:
            now = int(x.split('/')[0])
        else:
            now = int(x)
        temp = num = (1800 - now) / 360
        while True:
            if 0 <= temp <= 1:
                break
            temp = temp - 1
        if temp < 0.8:
            re = math.floor(num)
        else:
            re = math.ceil(num)
        return now, re

    # 利用ocr寻找关卡位置
    @staticmethod
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
            ch_names = dic[left][0]
            list = []
            list1 = [(93, 237), (308, 436), (512, 651), (723, 852), (930, 1064), (1137, 1270)]
            list2 = [(633, 766), (841, 972), (1048, 1181)]
            GamePassStep.goto_ahead_for_ziyuanshouji()
            re = base.screen(memery=True)
            list = list1
            for i in range(2):
                for item in list:
                    temp = base.cut(re, item[0], 460, item[1], 494)
                    res = base.ocr_without_position(temp, None, base.ziyuanshouji_tag)[0]["words"]
                    if res == ch_names:
                        logger.info("识别到关卡%s", name)
                        ck = (item[0], 460, item[1], 494)
                        base.randomClick(ck)
                        return ck
                GamePassStep.goto_behind_for_ziyuanshouji()
                re = base.screen(memery=True)
                list = list2
            logger.error("未找到关卡%s", name)
            raise module.error.game.GameNotFound(name)
            # 是否找到位置  0暂时未找到 1找到 -1找不到
        if type == "zhuxian" or type == "huodong":
            flag = 0
            while True:
                logger.info("尝试寻找关卡%s", name)
                list = GamePassStep.stage()
                if temp == list:
                    flag = -1
                    break
                if name in list:
                    logger.info("识别到关卡%s", name)
                    base.click(list[name][0], list[name][1])
                    return
                if flag == 1:
                    break
                temp = list
                base.scroll(1000, 40, 760, 43, 200)
                time.sleep(base.sleep_time)

            if flag == -1:
                logger.error("未找到关卡%s", name)
                for i in range(6):
                    base.scroll(600, 40, 1000, 43, 200)
                    time.sleep(base.sleep_time)

                raise module.error.game.GameNotFound(name)
            ck = (x1, y1, x2, y2)
            base.randomClick(ck)
            return ck

    # 利用模板匹配寻找关卡位置
    @staticmethod
    @retry(stop_max_attempt_number=2)
    def find_game_position_with_template(name, type="zhuxian"):
        # 随机点击关卡的位置区域
        x1 = 0
        x2 = 0
        y1 = 0
        y2 = 0
        flag = -1
        if type == "zhuxian" or type == "huodong":
            flag = 0
            times = 0
            while True:
                logger.info("尝试寻找关卡%s", name)
                det = base.template_match_best("/map/" + name + ".png")
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
                base.scroll(1000, 40, 760, 43, 200)
                time.sleep(base.sleep_time)
                if times > 20:
                    flag = -1
                    break
                times = times + 1
        if flag == -1:
            logger.error("未找到关卡%s", name)
            for i in range(6):
                base.scroll(600, 40, 1000, 43, 200)
                time.sleep(base.sleep_time)

            raise module.error.game.GameNotFound(name)
        base.randomClick((x1, y1, x2, y2))


if __name__ == '__main__':
    GamePassStep.jiaomieIsFinish()
