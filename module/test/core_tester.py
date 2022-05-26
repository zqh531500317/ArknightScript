import unittest
import warnings
from module.base import *


def my_annotation(**kwds):
    def decorate(fn):
        for item in kwds.items():
            key = item[0]
            value = item[1]
            fn.__annotations__[key] = value
        return fn

    return decorate


class TestScreen(unittest.TestCase):
    screen_n = 20

    adb = base.adb
    img = base.screen(memery=True)

    def setUp(self) -> None:
        warnings.simplefilter("ignore", ResourceWarning)
        base.screen(memery=False)

    @my_annotation(desc="adb截图测试")
    @bench_time(screen_n)
    def test_screen_adb(self):
        for i in range(self.screen_n):
            base._screen_adb()

    @my_annotation(desc="adb_nc截图测试")
    @bench_time(screen_n)
    def test_screen_adb_nc(self):
        for i in range(self.screen_n):
            base._screen_adb_nc()

    @my_annotation(desc="截图至cache")
    @bench_time(1)
    def test_screen(self):
        base.screen(memery=False)

    @my_annotation(desc="模板匹配测试")
    @bench_time(screen_n)
    def test_template_match(self):
        for i in range(self.screen_n):
            base.is_template_match("isInReason.png", screen_re=TestScreen.img)

    @my_annotation(desc="ocr测试")
    @bench_time(screen_n)
    def test_ocr(self):
        for i in range(self.screen_n):
            base.ocr(OcrEntity(input_img=TestScreen.img))


if __name__ == '__main__':
    ...
