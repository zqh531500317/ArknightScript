import os


# 定义配置基类


class Config:

    # 额外的初始化操作
    @staticmethod
    def init_app(app):
        os.system('chcp 65001')

        app.jinja_env.variable_start_string = '<<'
        app.jinja_env.variable_end_string = '>>'
        app.jinja_env.auto_reload = True
        app.config['SECRET_KEY'] = "secret_key"
