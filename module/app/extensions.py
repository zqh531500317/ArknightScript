import _thread

from flask_cors import CORS
from flask_socketio import SocketIO
from flask_login import LoginManager
from module.base import *

cors = CORS(supports_credentials=True)
name_space = "/dcenter"
socketio = SocketIO(cors_allowed_origins='*', async_mode='threading')
login_manager = LoginManager()


# websocket部分
@socketio.on('connect', namespace=name_space)
def connect():
    _thread.start_new_thread(send, ())


@socketio.on('disconnect', namespace=name_space)
def disconnect():
    print("disconnect")


def send():
    event_name = "dcenter"
    logfile = base.project_path + "/log/log.log"
    file = open(logfile, 'r', encoding='utf-8')
    file.read()
    socketio.emit(event_name, {'data': "连接到websocket"}, broadcast=False, namespace=name_space)
    while True:
        where = file.tell()
        line = file.readline()
        if not line:
            time.sleep(1)
            file.seek(where)
        else:
            data = {'data': line}
            socketio.emit(event_name, data, broadcast=False, namespace=name_space)


# 初始化
def config_extensions(app):
    cors.init_app(app)
    socketio.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'app_main.login'
    login_manager.login_message_category = 'info'
    login_manager.login_message = 'Access denied.'