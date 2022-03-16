import _thread
import time

from logzero import logger
from functools import wraps


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info("task %s is started", func.__name__)
        res = func(*args, **kwargs)
        logger.info("task %s is finished", func.__name__)
        return res

    return wrapper


def debug(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        import module.task.state
        module.task.state.debug_run = True
        _thread.start_new_thread(__sr, (func.__name__,))
        res = func(*args, **kwargs)
        module.task.state.debug_run = False
        return res

    return wrapper


def __sr(kind):
    while True:
        import module.utils.core_control
        import module.task.state
        if not module.task.state.debug_run:
            return
        module.utils.core_control.screen(path="/screenshots/debug/" + str(kind) + "/" + str(time.time()) + ".png")
        time.sleep(3)
