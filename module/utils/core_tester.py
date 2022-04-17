from module.utils.core_control import Adb
from module.utils.core_decoratir import bench_time
import unittest
import module.step.judge_step
import module.step.click_step
import warnings
from logzero import setup_default_logger


class TestScreen(unittest.TestCase):
    screen_n = 20

    adb = Adb()

    def setUp(self) -> None:
        warnings.simplefilter("ignore", ResourceWarning)
        setup_default_logger(disableStderrLogger=True)

    @bench_time(screen_n)
    def test_screen_adb(self):
        for i in range(self.screen_n):
            TestScreen.adb._screen_adb()

    @bench_time(screen_n)
    def test_screen_adb_nc(self):
        for i in range(self.screen_n):
            TestScreen.adb._screen_adb_nc()


class Testa(unittest.TestCase):
    def setUp(self) -> None:
        warnings.simplefilter("ignore", ResourceWarning)
        setup_default_logger(disableStderrLogger=True)

    def test_jijian_backto_main(self):
        module.step.judge_step.ensureGameOpenAndInMain()
        module.step.click_step.into_jijian()
        module.step.judge_step.ensureGameOpenAndInMain()
        self.assertTrue(module.step.judge_step.isInMain())


if __name__ == '__main__':
    unittest.main()
