import unittest
import warnings
from logzero import setup_default_logger
from module.base import *
from module.entity.ocr_entity import OcrEntity
from module.step.common_step import CommonStep
import module.task.daily
from module.step.recruit_step import RecruitStep
import module.task.fight
import module.task.jijian
import module.task.zhuxian


class TestTask(unittest.TestCase):

    def setUp(self) -> None:
        warnings.simplefilter("ignore", ResourceWarning)
        # setup_default_logger(disableStderrLogger=True)

    def test_recruit(self):
        CommonStep.ensureGameOpenAndInMain()
        CommonStep.dowait("main_recruit", "/recruit/main.png", description="进入公招界面")
        num = RecruitStep.get_recruit_num()
        logger.info("num=%s", num)
        r = module.task.daily.once_recruit(1)
        CommonStep.ensureGameOpenAndInMain()
        CommonStep.dowait("main_recruit", "/recruit/main.png", description="进入公招界面")
        num1 = RecruitStep.get_recruit_num()
        logger.info("num1=%s", num1)
        if r == -2 or r == 999:
            self.assertEquals(num1, num)
        else:
            self.assertEquals(num - 1, num1)

    def test_buy_xinyong_shop(self):
        CommonStep.ensureGameOpenAndInMain()
        CommonStep.dowait("main_shop", CommonStep.isInShop, "进入商店")
        CommonStep.dowait((1125, 93, 1257, 115), "/shop/main_xinyong.png", "进入信用商店")
        res1 = base.ocr_number(OcrEntity(x1=1158, y1=28, x2=1201, y2=50)).string
        logger.info("res1=%s", res1)
        module.task.daily.buy_xinyong_shop()
        CommonStep.ensureGameOpenAndInMain()
        CommonStep.dowait("main_shop", CommonStep.isInShop, "进入商店")
        CommonStep.dowait((1125, 93, 1257, 115), "/shop/main_xinyong.png", "进入信用商店")
        res2 = base.ocr_number(OcrEntity(x1=1158, y1=28, x2=1201, y2=50)).string
        logger.info("res2=%s", res2)
        self.assertTrue(int(res2) < 300)

    def test_friend(self):
        module.task.daily.friend()

    def test_receive_renwu(self):
        module.task.daily.receive_renwu()

    def test_receive_xinyong(self):
        module.task.daily.receive_xinyong()

    def test_zhuxian(self):
        module.task.zhuxian.zhuxian("1-7", 2)

    def test_clue(self):
        module.task.jijian.clue()

    def test_jijian_receive(self):
        module.task.jijian.jijian_receive()

    def test_use_electricity(self):
        module.task.jijian.use_electricity()
