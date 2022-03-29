import time

import module.task.daily
import module.task.huodong
import module.task.jijian
import module.schedule.dailyScheduler
import module.task.state
import module.utils.core_control
import module.utils.core_template
from module.utils.core_init import init
from module.utils.core_control import screen
from module.utils.core_ocr import *
from module.utils.core_picture import *
from module.utils.core_template import *
from PIL import Image
import module.step.recruit_step
from cnstd import CnStd
import cv2
import module.step.jijian_step
import module.step.judge_step
import logging
import os
import sys
from logzero import LogFormatter, setup_default_logger, logfile, logger
from module.utils.core_config import configList


def init_log():
    # 日志等级
    level_str = configList["Config"]["Log"]["level"]
    level = logging.INFO
    if level_str == "DEBUG":
        level = logging.DEBUG
    elif level_str == "INFO":
        level = logging.INFO
    elif level_str == "WARNING":
        level = logging.WARNING
    elif level_str == "ERROR":
        level = logging.ERROR
    elif level_str == "CRITICAL":
        level = logging.CRITICAL
    # 时间格式
    data_style = '%Y-%m-%d %H:%M:%S'

    # 控制台输出格式
    handler_format = '%(color)s[%(asctime)s| %(levelname)s |%(filename)s:%(lineno)d] %(message)s%(end_color)s'
    hand_format = LogFormatter(fmt=handler_format, datefmt=data_style)
    if configList["Config"]["Log"]["handler"]:
        setup_default_logger(formatter=hand_format, level=level, disableStderrLogger=False)
    else:
        setup_default_logger(formatter=hand_format, level=level, disableStderrLogger=True)

    # 文件输出格式
    if configList["Config"]["Log"]["file"]:
        file_format = '[%(asctime)s| %(levelname)s |%(filename)s:%(lineno)d] %(message)s'
        formatter = logging.Formatter(file_format, data_style)
        dic_path = configList["Config"]["System"]["project_path"] + '/log/'

        if not os.path.exists(configList["Config"]["System"]["project_path"] + '/cache/'):
            os.mkdir(configList["Config"]["System"]["project_path"] + '/cache/')
        logfile(dic_path + 'log.log',
                formatter=formatter,
                maxBytes=1e6, encoding='utf-8', loglevel=level)
    logger.info("初始化日志配置")


init_log()


def test_daily():
    module.task.daily.friend()
    module.task.daily.receive_renwu()
    module.task.daily.receive_xinyong()
    module.task.daily.recruit_daily()
    module.task.daily.buy_xinyong_shop()


def test_fight():
    module.task.huodong.huodong("GA-8", 99, False, 0, False, 0)


def test_jijian():
    module.task.jijian.jijian_receive()
    module.task.jijian.use_electricity()


def test_control():
    avg_time = 0
    times = 10
    for i in range(times):
        begin_time = time.time()
        screen(memery=False)
        end_time = time.time()
        run_time = end_time - begin_time
        avg_time = avg_time + run_time
    print(avg_time / times)


class Tester(Adb):
    screen_n = 20

    def __init__(self):
        super().__init__()

    @bench_time(screen_n)
    def test_screen(self):
        for i in range(self.screen_n):
            screen(memery=True)


if __name__ == '__main__':
    # module.task.daily.xinpian()
    test_daily()

    # region = read(screen_path)
    # cropped = cut(region, 766, 25, 863, 48)  # 基建无人机
    # cropped = cut(region, 585, 193, 687, 225)#判断剿灭是否打完
    # cropped = cut(region, 1187, 28, 1277, 52)  # 拜访好友是否变化
    # cropped =cut(region, 1116, 20, 1245, 57)  # 获取理智
    # write(screen_path,cropped)
    # ocr_without_position(screen_path)
