from flask import Blueprint, jsonify
from flask_login import login_required
from logzero import logger

from module.schedule.baseScheduler import base_scheduler

app_scheduler = Blueprint("app_scheduler", __name__)


# 暂停调度器
@app_scheduler.route('/pause_scheduler', methods=['get'])
@login_required
def pause_scheduler():
    base_scheduler.pause_scheduler()
    logger.info("暂停调度器")
    return jsonify({'result': "暂停中"})


# 恢复调度器
@app_scheduler.route('/resume_scheduler', methods=['get'])
@login_required
def resume_scheduler():
    base_scheduler.resume_scheduler()
    logger.info("恢复调度器")
    return jsonify({'result': "运行中"})


# 获取调度器状态  运行中、暂停中
@app_scheduler.route('/is_scheduler_running', methods=['get', 'post'])
def is_scheduler_running():
    state = base_scheduler.is_scheduler_running()
    # logger.debug("调度器状态为{}".format(state))
    return jsonify({'result': state})
