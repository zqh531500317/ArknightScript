import _thread

from module.base import *
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.cron import CronTrigger
from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO
import module.schedule.fightScheduler
import module.schedule.dailyScheduler
import module.schedule.jijianScheduler
from flask_cors import CORS
from engineio.async_drivers import threading
from module.schedule.baseScheduler import base_scheduler


def init():
    module.schedule.dailyScheduler.add_all()
    module.schedule.jijianScheduler.add_all()


init()

os.system('chcp 65001')
app = Flask(__name__, template_folder="webapp/resources", static_folder="webapp/resources", static_url_path="")
CORS(app, supports_credentials=True)
app.jinja_env.variable_start_string = '<<'
app.jinja_env.variable_end_string = '>>'
app.jinja_env.auto_reload = True
app.config['SECRET_KEY'] = 'secret_key'
socketio = SocketIO(app, cors_allowed_origins='*', async_mode='threading')
name_space = "/dcenter"


# 首页
@app.route('/')
def index():
    return render_template('index.html')


# 暂停调度器
@app.route('/pause_scheduler', methods=['get'])
def pause_scheduler():
    base_scheduler.pause_scheduler()
    logger.info("暂停调度器")
    return jsonify({'result': "暂停中"})


# 恢复调度器
@app.route('/resume_scheduler', methods=['get'])
def resume_scheduler():
    base_scheduler.resume_scheduler()
    logger.info("恢复调度器")
    return jsonify({'result': "运行中"})


# 获取调度器状态  运行中、暂停中
@app.route('/is_scheduler_running', methods=['get'])
def is_scheduler_running():
    state = base_scheduler.is_scheduler_running()
    # logger.debug("调度器状态为{}".format(state))
    return jsonify({'result': state})


# 执行任务
@app.route('/fight', methods=['post'])
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


@app.route('/recruit', methods=['post'])
def recruit():
    is_fight = base.state.is_fight

    if is_fight == "stop":
        base.state.is_fight = "fight"
        recruit = request.get_json()["recruit"]
        times = int(recruit["times"])
        module.schedule.dailyScheduler.once_recruit(times)
        return jsonify({'result': "success"})

    logger.warn("正在进行任务")
    return jsonify({'result': "正在进行任务请勿执行"})


@app.route("/reschedule_job", methods=['post'])
def reschedule_job():
    job = request.get_json()["job"]
    id = job["id"]
    hour = job["hour"]
    minute = job["minute"]
    trigger = CronTrigger(hour=hour, minute=minute)
    b = base_scheduler.reschedule_job(id, trigger)
    if b:
        return jsonify({'result': "success"})
    else:
        return jsonify({'result': "reschedule_job error"})


@app.route("/pause_or_resume", methods=['post'])
def pause_or_resume():
    name = request.get_json()["name"]
    state = bool(request.get_json()["state"])
    if state:
        base_scheduler.resume(name)
    else:
        base_scheduler.pause(name)
    return jsonify({'result': "success"})


@app.route("/trigger_change", methods=['post'])
def trigger_change():
    name = request.get_json()["name"]
    kind = request.get_json()["kind"]
    value = request.get_json()["value"]
    base_scheduler.reschedule_job_part(name, kind, value)
    return jsonify({'result': "success"})


# 获取状态
@app.route('/lizhi', methods=['get'])
def lizhi():
    result = base.state.lizhi
    return jsonify({'result': result})


@app.route('/get_jobs', methods=['get'])
def get_jobs():
    jobs = base_scheduler.get_jobs()
    result = []
    for s in jobs:
        if isinstance(s.trigger, CronTrigger):
            if s.next_run_time is None:
                next_run_time = "pause"
            else:
                next_run_time = s.next_run_time
            temp = {"id": s.id, "name": s.name, "next_run_time": next_run_time,
                    "hour": str(s.trigger.fields[5]), "minute": str(s.trigger.fields[6])}
            result.append(temp)
        elif isinstance(s.trigger, DateTrigger):
            temp = {"id": s.id, "name": s.name, "next_run_time": str(s.trigger.run_date),
                    "hour": "None", "minute": "None"}
            result.append(temp)
    return jsonify({'result': result})


@app.route('/get_job', methods=['post'])
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


@app.route('/get_fight_jobs', methods=['get'])
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
        temp = {"id": s.id, "state": state, "name": s.name,
                "hour": str(s.trigger.fields[5]),
                "minute": str(s.trigger.fields[6]),
                "day_of_week": str(s.trigger.fields[4]),
                "map_name": s.args[0],
                "times": s.args[1]
                }
        result.append(temp)
    return jsonify({'result': result})


@app.route('/running_task', methods=['get'])
def running_task():
    return jsonify({'result': base.state.running_task_name})


# 添加任务
@app.route('/add_fight_job', methods=['post'])
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
        module.schedule.fightScheduler.zhuxian(id, trigger, map_name, times)
    elif type == "资源收集":
        module.schedule.fightScheduler.ziyuanshouji(id, trigger, map_name, times)
    elif type == "剿灭":
        module.schedule.fightScheduler.jiaomie(id, trigger, map_name, times)
    elif type == "活动":
        module.schedule.fightScheduler.huodong(id, trigger, map_name, times)
    elif type == "最近的作战":
        module.schedule.fightScheduler.recently(id, trigger, times)

    return jsonify({'result': "success"})


@app.route('/del_fight_job', methods=['post'])
def del_fight_job():
    id = request.get_json()["id"]
    base_scheduler.scheduler.remove_job(id)

    return jsonify({'result': "success"})


# 打开config.yaml
@app.route('/alt_config', methods=['get'])
def alt_config():
    cmd = base.project_path + '\\config\\config.yaml'
    os.system(cmd)
    return jsonify({'result': "success"})


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


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", debug=False)
