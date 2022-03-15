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
