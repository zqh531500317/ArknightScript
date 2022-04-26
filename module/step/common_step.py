from module.base import *
from module.step.base_step import BaseStep
import module.error.game


class CommonStep(BaseStep):
    @staticmethod
    def isInLogin():
        return base.is_template_match("isLogining.png", template_threshold=0.9)

    @staticmethod
    def isFightEnd(game):
        time.sleep(base.get("sleep_time"))
        if game == "剿灭":
            b = base.is_template_match("/fight/end_jiaomie.png")
            if b:
                base.randomClick("end_jiaomie")
                time.sleep(base.get("sleep_time"))
                logger.info("战斗已结束，存储结算图片")
                img = base.screen(memery=True)
                path = base.save1("jiaomie", "get_items", img)
                if not os.path.exists(base.endFight_path[:base.endFight_path.rfind("/")]):
                    os.makedirs(base.endFight_path[:base.endFight_path.rfind("/")])
                shutil.copy(path, base.endFight_path)
            else:
                logger.debug("战斗未结束")
            return b > 0.8
        else:
            img = base.screen(memery=True)
            re = base.cut(img, 58, 180, 207, 256)
            res = base.ocr_without_position(re)[0]["words"]
            b = (res == '行动')
            if b:
                logger.info("战斗已结束，存储结算图片")
                time.sleep(base.get("sleep_time") * 2)
                img = base.screen(memery=True)
                path = base.save1(game, "get_items", img)
                if not os.path.exists(base.endFight_path[:base.endFight_path.rfind("/")]):
                    os.makedirs(base.endFight_path[:base.endFight_path.rfind("/")])
                shutil.copy(path, base.endFight_path)

            else:
                logger.debug("战斗未结束")
            return b

    @staticmethod
    def isFightFail():
        return base.compareSimilar("end_fight_fail") > 0.9

    @staticmethod
    def isLevelUp():
        img = base.screen(memery=True)
        re = base.cut(img, 291, 351, 381, 398)
        res = base.ocr_without_position(re, None, None)[0]["words"]
        return res == "等级"

    @staticmethod
    def isInMain():
        return base.is_template_match("/ui/main.png")

    @staticmethod
    def isInMessageAfterLogin():
        return base.compareSame("message_after_login")

    @staticmethod
    def isInMonthAfterLogin():
        return base.compareSimilar("month_after_login") > 0.9

    @staticmethod
    def isInTerminal():
        return base.compareSame("terminal")

    @staticmethod
    def is_in_jijian_main():
        return base.is_template_match("jijian/jijian_main.png")

    # 是否在理智恢复界面
    @staticmethod
    def isInReason():
        return base.is_template_match("isInReason.png")

    # 是否在作战前界面
    @staticmethod
    def isInPreFight():
        return base.is_template_match("pre_fight.png")

    @staticmethod
    def isInShop():
        return base.is_template_match("/shop/main.png")

    @staticmethod
    def ensureGameOpen():
        if not base.isLive():
            CommonStep.into_login()

    @staticmethod
    def ensureGameOpenAndInMain():
        CommonStep.into_login()

    @staticmethod
    def into_jijian():
        CommonStep.ensureGameOpenAndInMain()
        CommonStep.dowait((1000, 625, 1001, 626), "jijian/jijian_main.png", description="进入基建页面")

    @staticmethod
    def into_main():
        if CommonStep.isInMain():
            return
        CommonStep.dowait("terminal", "terminal_go_home.png")
        base.randomClick("terminal_go_home")
        while True:
            if base.is_template_match("/ui/main.png"):
                break
            if base.is_template_match("/jijian/go_home_from_construction.png"):
                base.randomClick("go_home_from_construction")
            time.sleep(base.sleep_time)
        logger.info('到主界面')

    # 登录:
    @staticmethod
    def into_login():
        if not base.isLive():
            logger.info("尝试登陆游戏")
            base.start()
            CommonStep.dowait("", "/ui/isLogining.png", description="到登录界面", retry_time=60)
            CommonStep.dowait("login", "/ui/main.png", description="到主界面", retry_time=60)
        else:
            CommonStep.into_main()

    # 关闭游戏弹框
    @staticmethod
    def close_alert():
        det = base.template_match_best('close_ui.png')
        if len(det) != 0 and det[4] >= 0.95:
            x1 = det[0]
            y1 = det[1]
            x2 = det[2]
            y2 = det[3]
            base.randomClick((x1, y1, x2, y2))
            time.sleep(base.sleep_time)

        det = base.template_match_best('get_items.png', 514, 0, 758, 720)
        if len(det) != 0 and det[4] >= 0.8:
            x1 = det[0]
            y1 = det[1]
            x2 = det[2]
            y2 = det[3]
            base.randomClick((x1, y1, x2, y2))

    @staticmethod
    def into_Fight():
        base.click(1150, 660)
        while True:
            if CommonStep.isInReason():
                return False
            else:
                if base.is_template_match("/ensure_fight.png"):
                    base.randomClick("ensure_fight")
                    logger.info("开始作战")
                    return True
            time.sleep(base.sleep_time)

    @staticmethod
    def out_jijian():
        base.click(90, 38)
        base.click(875, 495)
        logger.info("退出基建页面")

    @staticmethod
    def out_Fight():
        base.click(600, 300)
        logger.info("退出奖励结算界面")

    @staticmethod
    def out_fight_fail():
        base.randomClick((1007, 316, 1056, 340))
        time.sleep(3 * base.sleep_time)
        base.click(600, 300)

    @staticmethod
    def choosedailizhihui(game):
        logger.info("启用代理指挥")
        img = base.screen(memery=True)
        rgb = base.getRGB(1066, 604, img)
        if not (rgb[0] >= 200 and rgb[1] >= 200 and rgb[2] >= 200):
            base.click(1066, 604)
        time.sleep(base.sleep_time)
        img = base.screen(memery=True)
        rgb = base.getRGB(1066, 604, img)
        if not (rgb[0] >= 200 and rgb[1] >= 200 and rgb[2] >= 200):
            raise module.error.game.CanNotChooseDaiLiZhiHui(game)

    # return 1表示吃药 2表示碎石 todo 碎石
    @staticmethod
    def use_medicine_or_stone(use_medicine, medicine_num, use_stone, stone_num):
        if use_medicine and medicine_num > 0:
            if base.compareSimilar("use_medicine_before_fight") < 0.9:
                raise module.error.game.ErrorPage()
            base.randomClick("use_medicine_before_fight")
            time.sleep(base.sleep_time)
            return 1
        # 随便点个地方退出理智补充界面
        base.click(1247, 500)
