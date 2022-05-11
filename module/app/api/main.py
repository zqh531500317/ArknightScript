from flask import Blueprint, jsonify, request, render_template, flash, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user

from module.app.extensions import login_manager
from module.entity.user import query_user, User, add_user
from logzero import logger

app_main = Blueprint("app_main", __name__)


@login_manager.request_loader
def load_user_from_request(request):
    ip = request.remote_addr
    user = User(ip)
    if not user.is_authenticated:
        logger.info("access ip=%s", ip)
    if "192.168.1.1" == ip:
        return None
    if "192.168.1" in ip or "127.0.0.1" in ip or "localhost" in ip:
        # logger.info("aaa")
        add_user(ip)
        login_user(user)
        return user
    else:
        # logger.info("bbb")
        return None


# 首页
@app_main.route('/')
@login_required
def index():
    # logger.info(request.remote_addr)
    return render_template('index.html')


@app_main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        l1 = request.get_json()["user"]
        user_id = l1('userid')
        user = query_user(user_id)

        if user is not None and l1['password'] == user['password']:
            # 通过Flask-Login的login_user方法登录用户
            login_user(User(user_id))
            return jsonify({'result': True})
        else:
            flash('Wrong username or password!')
            return jsonify({'result': False})
    # GET 请求
    ip = request.remote_addr
    if "192.168.1.1" == ip:
        return render_template('login.html')
    if "192.168.1" in ip or "127.0.0.1" in ip or "localhost" in ip:
        # add_user(ip)
        # login_user(User(ip))
        return redirect(url_for('app_main.index'))
    return render_template('login.html')


@app_main.route('/logout')
@login_required
def logout():
    print("logout")
    logout_user()
    return jsonify({'result': 'Logged out successfully!'})


@app_main.route('/isLogin', methods=['get'])
def isLogin():
    ip = request.remote_addr
    user = User(ip)
    return jsonify({'result': user.is_authenticated})
