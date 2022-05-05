import os
from flask import Blueprint, jsonify, Response
from flask_login import login_required
from module.base import *

app_other = Blueprint("app_other", __name__)


# 打开config.yaml
@app_other.route('/alt_config', methods=['get'])
@login_required
def alt_config():
    cmd = base.project_path + '\\config\\config.yaml'
    os.system(cmd)
    return jsonify({'result': "success"})


@app_other.route('/shutdown', methods=['get'])
@login_required
def shutdown():
    logger.info("shutdown App")
    logger.info("==============================")
    os._exit(0)
