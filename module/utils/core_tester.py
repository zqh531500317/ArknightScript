from module.utils.core_control import Adb
from module.utils.core_decoratir import bench_time


class Tester:
    screen_n = 20

    def __init__(self):
        self.adb = Adb()

    def test_screen(self):
        self.__screen_adb()
        self.__screen_adb_nc()

    @bench_time(screen_n)
    def __screen_adb(self):
        for i in range(self.screen_n):
            self.adb._screen_adb()

    @bench_time(screen_n)
    def __screen_adb_nc(self):
        for i in range(self.screen_n):
            self.adb._screen_adb_nc()
