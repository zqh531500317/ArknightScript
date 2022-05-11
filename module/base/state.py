from module.base.decorator import singleton


@singleton
class State:
    is_config_edit = False
    lizhi = {"time": "0", "lizhi": "0", "maxlizhi": "0"}
    is_fight = "stop"  # stop or running or task(标记不能同时运行的任务)
    running_task_num = 0
    debug_run = False
    running_task_name = ""
