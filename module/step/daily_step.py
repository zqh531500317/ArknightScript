import copy
import module.error.game
from datetime import datetime

from module.entity.ocr_entity import OcrEntity
from module.inventory.demo import show_bag
from module.penguin_stats.core import analyse, get_name_by_id
from module.base import *
from module.step.fight_step import FightStep
from module.step.gamepass_step import GamePassStep


class DailyStep:
    @staticmethod
    def receive_daily_renwu():
        if base.compareSimilar("daily_renwu") >= 0.9:
            base.randomClick("daily_renwu")
            time.sleep(base.sleep_time)
            base.randomClick("renwu_receive")
            time.sleep(base.sleep_time)
            base.click(638, 645)

    @staticmethod
    def receive_weekly_renwu():
        if base.compareSimilar("weekly_renwu") >= 0.9:
            base.randomClick("weekly_renwu")
            time.sleep(base.sleep_time)
            base.randomClick("renwu_receive")
            time.sleep(base.sleep_time)
            base.click(638, 645)

    @staticmethod
    def friend_home():
        time.sleep(2 * base.sleep_time)
        region = base.screen(memery=True)
        cropped = base.cut(region, 1187, 28, 1277, 52)
        ocr_entity = OcrEntity(input_img=cropped, cand_alphabet=base.number_tag, except_result="")
        result = base.ocr(ocr_entity)
        pre = result[0]["words"]
        while True:
            base.randomClick("friend_home")
            time.sleep(3 * base.sleep_time)
            region = base.screen(memery=True)
            cropped = base.cut(region, 1187, 28, 1277, 52)
            ocr_entity = OcrEntity(input_img=cropped, cand_alphabet=base.number_tag, except_result="")
            result = base.ocr(ocr_entity)
            later = result[0]["words"]
            if pre == later:
                return
            pre = later

    @staticmethod
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

    @staticmethod
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
                map_name = DailyStep.__get_map_name(k)
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

    @staticmethod
    def get_xinpian_info(xinpian_1=6, xinpian_2=10):
        base.randomClick("main_cangku")
        time.sleep(base.sleep_time)
        bag_info = DailyStep.__get_bag_info()
        xinpian_info = {}
        for name, v in bag_info.items():
            num = v["num"]
            map_name = DailyStep.__get_map_name(name)
            if map_name is None:
                continue
            xinpian_info[name] = {"num": num, "map_name": map_name}
        logger.debug("精二芯片每种目标数量:%s 精一芯片每种目标数量:%s", xinpian_2, xinpian_2)
        logger.debug("=======仓库芯片信息=======")
        for k, v in xinpian_info.items():
            logger.debug("  %s  %s", k, str(v))
        queshao_info = DailyStep.__cal_by_data(copy.deepcopy(xinpian_info), xinpian_1, xinpian_2)

        logger.debug("=======缺少芯片信息=======")
        for k, v in queshao_info.items():
            logger.info("  %s  %s", k, str(v))
        return xinpian_info, queshao_info

    @staticmethod
    def __get_bag_info():
        bag_info = {}
        pre_items = None
        while True:
            items = show_bag()
            later_items = items.keys()
            if pre_items == later_items:
                break
            bag_info.update(items)
            base.scroll(1240, 475, 465, 475, 3000)
            pre_items = later_items
        return bag_info

    # res 缺少芯片信息
    @staticmethod
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
                    FightStep.fight(game_name, False, 0, False, 0)
                    if not fightTime.get(game_name):
                        fightTime[game_name] = 1
                    else:
                        fightTime[game_name] += 1
                    logger.info("进行一场{}".format(game_name))
                    # 获取战斗掉落信息
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
                    if queshao_info.get(drop_name):
                        queshao_info[drop_name]['num'] -= 1
                    if not getTime.get(drop_name):
                        getTime[drop_name] = 1
                    else:
                        getTime[drop_name] += 1
                    time.sleep(base.sleep_time)
        except module.error.game.CanNotChooseDaiLiZhiHui as e:
            e.message()
        except module.error.game.NotInPreFight as e:
            e.message()
        except module.error.game.GameFail as e:
            e.message()
        except module.error.game.NotReason as e:
            e.message()
        except module.error.game.ErrorPage as e:
            e.message()
            base.stop()
        finally:
            logger.info("=======刷图情况=======")
            for k, v in fightTime.items():
                logger.info("%s %s", k, v)
            logger.info("=======芯片获取情况=======")
            for k, v in getTime.items():
                logger.info("%s %s", k, v)
            base.send('刷芯片完成', '刷图情况:' + str(fightTime) + "\r\n" +
                      '芯片获取情况:' + str(getTime))
