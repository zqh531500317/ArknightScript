from apscheduler.triggers.cron import CronTrigger
from flask import Blueprint, jsonify, request
from flask_login import login_required
from module.schedule.baseScheduler import base_scheduler
import module.schedule.fightScheduler
import module.schedule.dailyScheduler
import module.schedule.jijianScheduler
from module.base import *

app_task = Blueprint("app_task", __name__)


# 执行任务
@app_task.route('/fight', methods=['post'])
@login_required
def fight():
    # stop：停止状态可执行，start：正在作战
    is_fight = base.state.is_fight
    use_medicine = use_stone = False
    medicine_num = stone_num = 0
    if is_fight == "stop":
        fight = request.get_json()["fight"]
        name = fight["name"]
        type = fight["type"]
        times = int(fight["times"])
        use_medicine = bool(fight["use_medicine"])
        medicine_num = int(fight["medicine_num"])
        use_stone = bool(fight["use_stone"])
        stone_num = int(fight["stone_num"])
        # 执行
        if type == "主线":
            module.schedule.fightScheduler.once_zhuxian(name, times, use_medicine, medicine_num, use_stone, stone_num)
        elif type == "资源收集":
            module.schedule.fightScheduler.once_ziyuanshouji(name, times, use_medicine, medicine_num, use_stone,
                                                             stone_num)
        elif type == "剿灭":
            module.schedule.fightScheduler.once_jiaomie(times, use_medicine, medicine_num, use_stone, stone_num)
        elif type == "未适配作战":
            module.schedule.fightScheduler.once_unknown(times, use_medicine, medicine_num, use_stone, stone_num)
        elif type == "活动":
            module.schedule.fightScheduler.once_huodong(name, times, use_medicine, medicine_num, use_stone, stone_num)
        elif type == "最近的作战":
            module.schedule.fightScheduler.once_recently(name, times, use_medicine, medicine_num, use_stone, stone_num)

        return jsonify({'result': "success"})

    logger.warn("正在进行fight")
    return jsonify({'result': "正在作战请勿再次作战"})


@app_task.route('/recruit', methods=['post'])
@login_required
def recruit():
    is_fight = base.state.is_fight
    recruitEntity = request.get_json()["recruitEntity"]
    if is_fight == "stop":
        base.state.is_fight = "task"
        num = int(recruitEntity["num"])
        module.schedule.dailyScheduler.once_recruit(num)
        return jsonify({'result': "success"})

    logger.warn("正在进行任务")
    return jsonify({'result': "正在进行任务请勿执行"})


@app_task.route("/reschedule_job", methods=['post'])
@login_required
def reschedule_job():
    job = request.get_json()["job"]
    id = job["id"]
    hour = str(job["hour"]).replace("，", ",")
    minute = str(job["minute"]).replace("，", ",")
    trigger = CronTrigger(hour=hour, minute=minute)
    b = base_scheduler.reschedule_job(id, trigger)
    if b:
        return jsonify({'result': "success"})
    else:
        return jsonify({'result': "reschedule_job error"})


@app_task.route("/pause_or_resume", methods=['post'])
@login_required
def pause_or_resume():
    name = request.get_json()["name"]
    state = bool(request.get_json()["state"])
    if state:
        base_scheduler.resume(name)
    else:
        base_scheduler.pause(name)
    return jsonify({'result': "success"})


@app_task.route("/trigger_change", methods=['post'])
@login_required
def trigger_change():
    name = request.get_json()["name"]
    kind = request.get_json()["kind"]
    value = request.get_json()["value"]
    base_scheduler.reschedule_job_part(name, kind, value)
    return jsonify({'result': "success"})
