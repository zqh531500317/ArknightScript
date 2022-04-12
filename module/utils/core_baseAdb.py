import adbutils

from module.utils.core_config import CoreConfig
from logzero import logger
from retrying import retry


class BaseAdb:
    def __init__(self):
        logger.debug("初始化BaseAdb")
        self.cf = CoreConfig()
        self.adb_client = adbutils.AdbClient('127.0.0.1', 5037)
        self.connect()
        self.adb = adbutils.AdbDevice(self.adb_client, self.cf.serial)

    @retry(stop_max_attempt_number=3)
    def connect(self):
        msg = self.adb_client.connect(self.cf.serial)
        logger.info(msg)

    def disconnect(self):
        msg = self.adb_client.disconnect(self.cf.serial)
        logger.info(msg)

    def start(self):
        self.stop()
        self.adb.app_start(self.cf.package_name, self.cf.activity_name)
        logger.info("启动应用%s", self.cf.package_name)

    def stop(self):
        self.adb.app_stop(self.cf.package_name)
        logger.info("关闭应用%s", self.cf.package_name)

    def isLive(self):
        text = self.adb.current_app()["package"]
        if self.cf.package_name == text:
            return True
        return False
