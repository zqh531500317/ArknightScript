from flask import Flask

from module.app.config import Config
from module.app.extensions import config_extensions
from module.app.api import config_blueprint
from module.schedule import config_scheduler
from module.base import base


def create_app():
    app = Flask(__name__, template_folder=base.project_path + "/webapp/resources",
                static_folder=base.project_path + "/webapp/resources",
                static_url_path="")
    Config.init_app(app)
    # 加载扩展
    config_extensions(app)
    # 配置蓝本
    config_blueprint(app)
    # 配置调度器
    config_scheduler()
    # 返回app实例对象
    return app
