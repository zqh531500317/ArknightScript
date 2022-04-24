from logzero import logger
import _thread
import os
import time
from module.base.control import Adb
from module.base.decorator import singleton


@singleton
class Base(Adb):
    def __init__(self):
        super().__init__()
        logger.info("class Base __init__")
        self.init_dir()
        self.int_close_alerter()

    def init_dir(self):
        root = self.project_path
        dic_path = root + "/log/"
        if not os.path.exists(dic_path):
            os.makedirs(dic_path)
        dic_path = root + '/cache/'
        if not os.path.exists(dic_path):
            os.makedirs(dic_path)
        dic_path = root + '/screenshots/'
        if not os.path.exists(dic_path):
            os.makedirs(dic_path)

    def close_alert(self):
        import module.step.click_step
        while True:
            time.sleep(3)
            if self.isLive():
                module.step.click_step.close_alert()

    def int_close_alerter(self):
        _thread.start_new_thread(self.close_alert, ())


base = Base()
