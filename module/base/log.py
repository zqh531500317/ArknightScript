import logging
import os
import sys
from logzero import LogFormatter, setup_default_logger, logfile, logger, setup_logger
from module.base.config import CoreConfig
from module.utils.core_utils import project_root_path


class Log(CoreConfig):
    def __init__(self):
        super().__init__()
        self.ocr_logger = None
        self.logger = None
        self.init_ocr_logger()
        self.init_logger()

    def init_logger(self):
        logger.info("init_log")
        # 日志等级
        level = logging.INFO
        if self.get("level") == "DEBUG":
            level = logging.DEBUG
        elif self.get("level") == "INFO":
            level = logging.INFO
        elif self.get("level") == "WARNING":
            level = logging.WARNING
        elif self.get("level") == "ERROR":
            level = logging.ERROR
        elif self.get("level") == "CRITICAL":
            level = logging.CRITICAL
        # 时间格式
        data_style = '%m-%d %H:%M:%S'

        # 控制台输出格式
        handler_format = '%(color)s[%(asctime)s| %(levelname)s |%(filename)s:%(lineno)d] %(message)s%(end_color)s'
        hand_format = LogFormatter(fmt=handler_format, datefmt=data_style)
        if self.get("handler"):
            setup_default_logger(formatter=hand_format, level=level, disableStderrLogger=False)
        else:
            setup_default_logger(formatter=hand_format, level=level, disableStderrLogger=True)

        # 文件输出格式
        if self.get("file"):
            dic_path = project_root_path() + "/log/"
            file_format = '[%(asctime)s| %(levelname)s |%(filename)s:%(lineno)d] %(message)s'
            formatter = logging.Formatter(file_format, data_style)
            logfile(dic_path + 'log.log',
                    formatter=formatter,
                    maxBytes=1e6, encoding='utf-8', loglevel=level)
        logger.info("初始化日志配置")
        self.logger = logger

    def init_ocr_logger(self):
        # 日志等级
        level = logging.INFO
        if self.get("level") == "DEBUG":
            level = logging.DEBUG
        elif self.get("level") == "INFO":
            level = logging.INFO
        elif self.get("level") == "WARNING":
            level = logging.WARNING
        elif self.get("level") == "ERROR":
            level = logging.ERROR
        elif self.get("level") == "CRITICAL":
            level = logging.CRITICAL
        data_style = '%m-%d %H:%M:%S'
        handler_format = '%(color)s[%(asctime)s| %(levelname)s |%(filename)s:%(lineno)d] %(message)s%(end_color)s'
        hand_format = LogFormatter(fmt=handler_format, datefmt=data_style)
        if self.get("file"):
            logfile = project_root_path() + "/log/" + 'ocr.log'
        else:
            logfile = None
        self.ocr_logger = setup_logger(formatter=hand_format, logfile=logfile, level=level, disableStderrLogger=True)
