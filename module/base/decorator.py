import datetime
from functools import wraps
from logzero import logger
import time


def singleton(cls):
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]

    return inner


def before(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        from module.base.base import base
        from module.schedule.listener import listener
        time.sleep(base.ONE_MINUTES)
        task_name = base.state.running_job['name']
        logger.debug("caltime start task_name={}".format(task_name))
        listener.caltimemap[task_name]['start_time'] = datetime.datetime.now().replace(microsecond=0)
        logger.info("task %s is started", task_name)
        res = func(*args, **kwargs)
        return res

    return wrapper


def bench_time(n):
    def decorate(func):
        @wraps(func)
        def mywrap(*args, **kwargs):
            from module.base.base import base
            start = time.time()
            func(*args, **kwargs)
            end = time.time()
            res = "%-20s cost: %-5ss,times: %-2s,avg time: %-4ss" % (func.__name__, round(end - start, 2), n,
                                                                     round((end - start) / n, 2))
            base.logger.info(res)
            return res

        return mywrap

    return decorate


# 为方法提供注解
# 使用：
# class Test:
#    @my_annotation(desc="adb截图测试",a="aa")
#    def f_test():
#      print("run f")
# 读取:
# 1、方法
#     lis = inspect.getmembers(Test, inspect.isfunction)
#     for t in lis:
#         if "f_test" == t[0]:
#             fc_name = t[0]   # 函数名称
#             desc = t[1].__annotations__.get("desc")
#             a = t[1].__annotations__.get("a")

# 2、函数
# module.task.daily.receive_renwu.__annotations__.get("desc")
def my_annotation(**kwds):
    def decorate(fn):
        for item in kwds.items():
            key = item[0]
            value = item[1]
            fn.__annotations__[key] = value
        return fn

    return decorate
