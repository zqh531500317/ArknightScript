from flask_cors import CORS
from flask_socketio import SocketIO
from flask_login import LoginManager
from module.base import *
from engineio.async_drivers import threading

name_space = "/dcenter"
socketio = SocketIO(cors_allowed_origins='*', async_mode='threading')
login_manager = LoginManager()
thread = None


# websocket部分
@socketio.on('connect', namespace=name_space)
def connect():
    global thread
    if thread is None:
        thread = socketio.start_background_task(target=send)


@socketio.on('disconnect', namespace=name_space)
def disconnect():
    print("disconnect")


def send():
    event_name = "dcenter"
    logfile = base.project_path + "/log/log.log"
    file = open(logfile, 'r', encoding='utf-8')
    file.read()
    socketio.emit(event_name, {'data': "连接到websocket"}, broadcast=True, namespace=name_space)
    while True:
        where = file.tell()
        line = file.readline()
        if not line:
            time.sleep(1)
            file.seek(where)
        else:
            data = {'data': line}
            socketio.emit(event_name, data, broadcast=True, namespace=name_space)


# 初始化
def config_extensions(app):
    CORS(app, supports_credentials=True)
    socketio.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'app_main.login'
    login_manager.login_message_category = 'info'
    login_manager.login_message = 'Access denied.'
