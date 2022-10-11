import inspect
import logging
import os
import time

from logzero import LogFormatter, setup_default_logger, logfile, logger

import module.task.daily
import module.task.huodong
from module.base.base import base
from module.entity.ocr_entity import OcrEntity
from module.test.core_tester import TestScreen
import module.utils.core_utils


def init_log():
    # 日志等级
    level_str = base.configList["Config"]["Log"]["level"]
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
    if base.configList["Config"]["Log"]["handler"]:
        setup_default_logger(formatter=hand_format, level=level, disableStderrLogger=False)
    else:
        setup_default_logger(formatter=hand_format, level=level, disableStderrLogger=True)

    # 文件输出格式
    if base.configList["Config"]["Log"]["file"]:
        file_format = '[%(asctime)s| %(levelname)s |%(filename)s:%(lineno)d] %(message)s'
        formatter = logging.Formatter(file_format, data_style)
        dic_path = base.configList["Config"]["System"]["project_path"] + '/log/'

        if not os.path.exists(base.configList["Config"]["System"]["project_path"] + '/cache/'):
            os.mkdir(base.configList["Config"]["System"]["project_path"] + '/cache/')
        logfile(dic_path + 'log.log',
                formatter=formatter,
                maxBytes=1e6, encoding='utf-8', loglevel=level)
    logger.info("初始化日志配置")


init_log()


def test_daily():
    # module.task.daily.friend()
    # module.task.daily.receive_renwu()
    # module.task.daily.receive_xinyong()
    # module.task.daily.recruit_daily()
    # module.task.daily.buy_xinyong_shop()
    pass


def test_fight():
    # module.task.huodong.huodong("GA-8", 99, False, 0, False, 0)
    pass


def test_jijian():
    # module.task.jijian.jijian_receive()
    # module.task.jijian.use_electricity()
    pass


if __name__ == '__main__':
    base.screen(memery=False)
