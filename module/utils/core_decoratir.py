import _thread
import os
import time

import cv2
from logzero import logger
from functools import wraps

project_path = os.path.abspath('')


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

        return mywrap

    return decorate


def debug_recode(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        import module.task.state
        logger.info("debug_recode is start:%s", func.__name__)
        module.task.state.debug_run = True
        _thread.start_new_thread(__sr, (func.__name__,))
        res = func(*args, **kwargs)
        module.task.state.debug_run = False
        logger.info("debug_recode is end:%s", func.__name__)

        return res

    return wrapper


def __sr(kind):
    img_list = []
    path = project_path + "/screenshots/debug/" + str(time.time_ns()) + " " + str(kind)
    while True:
        import module.utils.core_control
        import module.task.state
        if not module.task.state.debug_run:
            for img in img_list:
                logger.info(img[0])
                cv2.imwrite(img[0], img[1])
            return
        temp = module.utils.core_control.screen(memery=True)
        if not os.path.exists(path):
            os.makedirs(path)
        img_list.append(
            [path + "/" + str(time.time_ns()) + ".jpg", temp])
        time.sleep(2)
