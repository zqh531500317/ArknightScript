from flask import Blueprint, jsonify
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
