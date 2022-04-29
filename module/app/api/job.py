from apscheduler.triggers.cron import CronTrigger
from flask import Blueprint, jsonify, request
from flask_login import login_required

from module.schedule import fightScheduler
from module.schedule.baseScheduler import base_scheduler

app_job = Blueprint("app_job", __name__)


# 添加任务
@app_job.route('/add_fight_job', methods=['post'])
@login_required
def add_fight_job():
    fight = request.get_json()["fight"]
    id = fight["id"]
    map_name = fight["map_name"]
    type = fight["type"]
    times = int(fight["times"])
    day_of_week = fight["day_of_week"]
    hour = fight["hour"]
    minute = fight["minute"]
    if day_of_week == "":
        day_of_week = None
    if hour == "":
        hour = None
    if minute == "":
        minute = None
    trigger = CronTrigger(day_of_week=day_of_week, hour=hour, minute=minute)
    if "fight_" != id[:6]:
        return jsonify({'result': "id不符合格式"})
        # 执行
    if type == "主线":
        fightScheduler.zhuxian(id, trigger, map_name, times)
    elif type == "资源收集":
        fightScheduler.ziyuanshouji(id, trigger, map_name, times)
    elif type == "剿灭":
        fightScheduler.jiaomie(id, trigger, map_name, times)
    elif type == "活动":
        fightScheduler.huodong(id, trigger, map_name, times)
    elif type == "最近的作战":
        fightScheduler.recently(id, trigger, times)

    return jsonify({'result': "success"})


@app_job.route('/del_fight_job', methods=['post'])
@login_required
def del_fight_job():
    id = request.get_json()["id"]
    base_scheduler.scheduler.remove_job(id)

    return jsonify({'result': "success"})
