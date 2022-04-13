import _thread
import time

from module.utils.core_utils import project_root_path
import os


def init_dir():
    root = project_root_path()
    dic_path = root + "/log/"
    if not os.path.exists(dic_path):
        os.makedirs(dic_path)
    dic_path = root + '/cache/'
    if not os.path.exists(dic_path):
        os.makedirs(dic_path)
    dic_path = root + '/screenshots/'
    if not os.path.exists(dic_path):
        os.makedirs(dic_path)


def close_alert():
    import module.step.click_step
    while True:
        time.sleep(3)
        module.step.click_step.close_alert()


def int_close_alerter():
    _thread.start_new_thread(close_alert, ())


def init():
    init_dir()
    import module.utils.core_log
    import module.schedule.dailyScheduler
    import module.schedule.jijianScheduler
    import module.utils.core_watchdog

    module.utils.core_log.init_log()
    module.utils.core_watchdog.init()
    module.schedule.dailyScheduler.add_all()
    module.schedule.jijianScheduler.add_all()
    int_close_alerter()
