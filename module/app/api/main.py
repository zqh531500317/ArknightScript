from flask import Blueprint, jsonify, request, render_template, flash, redirect, url_for
from flask_login import login_required, login_user, logout_user
from module.base import *
from module.entity.user import query_user, User, add_user

app_main = Blueprint("app_main", __name__)


# 首页
@app_main.route('/')
@login_required
def index():
    return render_template('index.html')


@app_main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form.get('userid')
        user = query_user(user_id)
        if user is not None and request.form['password'] == user['password']:
            # 通过Flask-Login的login_user方法登录用户
            login_user(User(user_id))
            return redirect(url_for('app_main.index'))
        flash('Wrong username or password!')
    # GET 请求
    ip = request.remote_addr
    logger.info(ip)
    if "192.168.1.1" == ip:
        return render_template('login.html')
    if "192.168.1" in ip or "127.0.0.1" in ip:
        add_user(ip)
        login_user(User(ip))
        return redirect(url_for('app_main.index'))
    return render_template('login.html')


@app_main.route('/logout')
@login_required
def logout():
    print("logout")
    logout_user()
    return jsonify({'result': 'Logged out successfully!'})
