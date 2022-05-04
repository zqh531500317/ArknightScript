import unittest
import warnings
from logzero import setup_default_logger
from module.base import *
from module.step.common_step import CommonStep


class TestScreen(unittest.TestCase):
    screen_n = 20

    adb = base.adb

    def setUp(self) -> None:
        warnings.simplefilter("ignore", ResourceWarning)
        setup_default_logger(disableStderrLogger=True)

    @bench_time(screen_n)
    def test_screen_adb(self):
        for i in range(self.screen_n):
            base._screen_adb()

    @bench_time(screen_n)
    def test_screen_adb_nc(self):
        for i in range(self.screen_n):
            base._screen_adb_nc()

    def test_screen(self):
        base.screen()


if __name__ == '__main__':
    unittest.main()
