from logzero import logger
import _thread
import os
import time

from module.base.ocr import OcrHandler
from module.base.template import Template
from module.base.decorator import singleton
import module.utils.core_utils


@singleton
class Base(Template, OcrHandler):
    def __init__(self):
        super().__init__()
        logger.info("class Base __init__")
        self.init_dir()
        self.init_close_alerter()

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
        import module.step.common_step
        while True:
            time.sleep(3)
            if self.isLive():
                module.step.common_step.CommonStep.close_alert()

    def init_close_alerter(self):
        _thread.start_new_thread(self.close_alert, ())

    def send(self, subject, contents):
        user = base.user
        password = base.password
        host = base.host
        receiver = base.receiver
        module.utils.core_utils.send(subject, contents, user, password, host, receiver)


base = Base()
