from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from flask import Blueprint, jsonify, request
from flask_login import login_required
from module.base import *
from module.schedule.baseScheduler import base_scheduler
from module.utils.core_utils import get_announce_by_str

app_state = Blueprint("app_state", __name__)


# 获取状态
@app_state.route('/lizhi', methods=['get'])
@login_required
def lizhi():
    result = base.state.lizhi
    return jsonify({'result': result})


@app_state.route('/get_jobs', methods=['get'])
@login_required
def get_jobs():
    jobs = base_scheduler.get_jobs()
    result = []
    for s in jobs:
        str_fc = s.func_ref
        desc = get_announce_by_str(str_fc, 'desc')
        if isinstance(s.trigger, CronTrigger):
            if s.next_run_time is None:
                next_run_time = "pause"
            else:
                next_run_time = s.next_run_time
            temp = {"id": s.id, "name": s.name, "next_run_time": next_run_time,
                    "hour": str(s.trigger.fields[5]), "minute": str(s.trigger.fields[6]),
                    "desc": desc}
            result.append(temp)
        elif isinstance(s.trigger, DateTrigger):
            temp = {"id": s.id, "name": s.name, "next_run_time": str(s.trigger.run_date),
                    "hour": "None", "minute": "None", "desc": desc}
            result.append(temp)
    return jsonify({'result': result})


@app_state.route('/get_job', methods=['post'])
@login_required
def get_job():
    ids = request.get_json()["ids"]
    for id in list(ids.keys()):
        job = base_scheduler.get_job(id)
        if not job:
            return jsonify({'result': None})
        if job.next_run_time is None:
            state = False
        else:
            state = True
        temp = {"id": job.id, "state": state, "name": job.name, "next_run_time": job.next_run_time,
                "hour": str(job.trigger.fields[5]), "minute": str(job.trigger.fields[6])}
        ids[id] = temp
        # logger.debug(str(ids))
    return jsonify({'result': ids})


@app_state.route('/get_fight_jobs', methods=['get'])
@login_required
def get_fight_jobs():
    jobs = base_scheduler.get_jobs()
    result = []
    for s in jobs:
        if "fight_" not in s.id:
            continue
        if s.next_run_time is None:
            state = False
        else:
            state = True
        str_fc = s.func_ref
        desc = get_announce_by_str(str_fc, 'desc')
        temp = {"id": s.id, "state": state, "name": s.name,
                "hour": str(s.trigger.fields[5]),
                "minute": str(s.trigger.fields[6]),
                "day_of_week": str(s.trigger.fields[4]),
                "map_name": s.args[0],
                "times": s.args[1],
                "desc": desc
                }
        result.append(temp)
    return jsonify({'result': result})


@app_state.route('/running_task', methods=['get'])
@login_required
def running_task():
    return jsonify({'result': base.state.running_task_name})


@app_state.route('/waiting_task_list', methods=['get'])
@login_required
def waiting_task_list():
    return jsonify({'result': "todo"})


@app_state.route('/is_fight', methods=['get'])
@login_required
def is_fighting():
    return jsonify({'result': base.state.is_fight})


@app_state.route('/state_info', methods=['get'])
@login_required
def state_info():
    state = base.state
    # print(state.running_job_num)
    # print(state.running_job)
    # print(state.blocking_jobs)
    # print(len(state.blocking_jobs))
    blocking_jobs_json = []
    for job in state.blocking_jobs:
        str_fc = job.func_ref
        desc = get_announce_by_str(str_fc, 'desc')
        blocking_jobs_json.append(
            {"id ": job.id,
             "name": job.name,
             "desc": desc,
             "next_run_time": job.next_run_time}
        )
    return jsonify({'result': {
        "running_job_num": state.running_job_num,
        "running_job": state.running_job,
        "blocking_jobs": blocking_jobs_json,
        "blocking_jobs_num": len(state.blocking_jobs)
    }})
