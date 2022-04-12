import _thread
import os
import time

import cv2
from logzero import logger
from functools import wraps
from module.utils.core_utils import project_root_path
import module.utils.core_config

project_path = project_root_path()


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info("task %s is started", func.__name__)
        start = time.time()
        res = func(*args, **kwargs)
        end = time.time()
        logger.info("task running cost: %s minutes", end - start)
        logger.info("task %s is finished", func.__name__)
        return res

    return wrapper


def bench_time(n):
    def decorate(func):
        @wraps(func)
        def mywrap(*args, **kwargs):
            start = time.time()
            func(*args, **kwargs)
            end = time.time()
            logger.info("%-20s cost: %-5ss,times: %-2s,avg time: %-4ss", func.__name__, round(end - start, 2), n,
                        round((end - start) / n, 2))

            print("%-20s cost: %-5ss,times: %-2s,avg time: %-4ss" % (func.__name__, round(end - start, 2), n,
                                                                     round((end - start) / n, 2)))

        return mywrap

    return decorate


def singleton(cls):
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]

    return inner


def debug_recode(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        import module.task.state
        logger.info("debug_recode is start:%s", func.__name__)
        module.task.state.debug_run = True
        if module.utils.core_config.cf.debug:
            _thread.start_new_thread(__sr, (func.__name__,))
        res = func(*args, **kwargs)
        module.task.state.debug_run = False
        logger.info("debug_recode is end:%s", func.__name__)

        return res

    return wrapper


def __sr(kind):
    img_list = []
    path = project_path + "/screenshots/debug/{}/{}".format(str(kind), str(int(time.time_ns() / 1000)))
    while True:
        import module.utils.core_control
        import module.task.state
        if not module.task.state.debug_run:
            logger.info("debug_recode 开始存储记录")
            i = 0
            for img in img_list:
                cv2.imwrite(img[0], img[1])
                i += 1
            logger.info("总共存储照片%s张,存储至/screenshots/debug/%s/%s", i, str(kind), str(int(time.time_ns() / 1000)))
            logger.info("debug_recode 存储记录完毕")
            return
        temp = module.utils.core_control.screen(memery=True)
        x, y = temp.shape[0:2]
        temp = cv2.resize(temp, (int(y / 2), int(x / 2)))
        if not os.path.exists(path):
            os.makedirs(path)
        img_list.append(
            [path + "/" + str(time.time_ns()) + ".jpg", temp])
        time.sleep(2)
