import os
import threading
import time

from flask import Blueprint, jsonify, Response
from flask_login import login_required
from module.base import *

app_system = Blueprint("app_system", __name__)


# 打开config.yaml
@app_system.route('/alt_config', methods=['get'])
@login_required
def alt_config():
    cmd = base.project_path + '\\config\\config.yaml'
    os.system(cmd)
    return jsonify({'result': "success"})


@app_system.route('/ping', methods=['get'])
def ping():
    return jsonify({'result': "success"})


@app_system.route('/shutdown', methods=['get'])
@login_required
def shutdown():
    def close():
        while True:
            logger.info("shutdown App after 5 minutes")
            time.sleep(5)
            logger.info("shutdown")
            os._exit(0)

    threading.Thread(target=close).start()
    return jsonify({'result': "success"})
