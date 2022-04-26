from module.base.decorator import singleton


@singleton
class State:
    is_config_edit = False
    lizhi = {"time": "0", "lizhi": "0", "maxlizhi": "0"}
    is_fight = "stop"
    running_task_num = 0
    debug_run = False
    running_task_name = ""
