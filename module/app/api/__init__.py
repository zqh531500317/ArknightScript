from module.app.api.scheduler import app_scheduler
from module.app.api.main import app_main
from module.app.api.task import app_task
from module.app.api.state import app_state
from module.app.api.job import app_job
from module.app.api.system import app_system
from module.app.api.test import app_test

DEFAULT_BLUEPRINT = (
    app_main, app_scheduler, app_task, app_state, app_job, app_system, app_test
)


def config_blueprint(app):
    # 循环读取元组中的蓝本
    for blueprint in DEFAULT_BLUEPRINT:
        app.register_blueprint(blueprint)
