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


class JijianSchudule(unittest.TestCase):
    def setUp(self) -> None:
        warnings.simplefilter("ignore", ResourceWarning)
        # setup_default_logger(disableStderrLogger=True)

    def test_jijian_schedule(self):
        before = base.read_json(base.project_path + "/config/schedual.json")
        module.task.jijian.schedual()
        after = base.read_json(base.project_path + "/config/schedual.json")

    def test_xinpian(self):
        module.task.daily.xinpian()
