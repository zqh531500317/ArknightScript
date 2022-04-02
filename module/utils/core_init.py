import os

import module.utils.core_log
import module.schedule.dailyScheduler
import module.schedule.jijianScheduler
from module.utils.core_utils import project_root_path
import module.utils.core_watchdog


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


def init():
    init_dir()
    module.utils.core_log.init_log()
    module.utils.core_watchdog.init()
    module.schedule.dailyScheduler.add_all()
    module.schedule.jijianScheduler.add_all()
