#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021-02-19 10:31
# @Site    : 
# @File    : JJInterface.py
# @Software: PyCharm
import os
import os
import sys
curPath = os.path.abspath(os.path.dirname(__file__))
print(curPath)
rootPath = os.path.split(curPath)[0] + '/'
print(rootPath)
sys.path.append(os.path.split(rootPath)[0])

from flask import Flask, request, jsonify, render_template

# 创建一个服务
from DB.JJSqlite import sqllitDBHelper

app = Flask(__name__, template_folder='../templates', static_folder='../static')


# 创建一个接口 指定路由和请求方法 定义处理请求的函数
@app.route('/login', methods=['GET'])
def everything():
    """
    请求登录页
    :return:
    """
    return render_template('index.html')


@app.route('/verification', methods=['post'])
def verification():
    """
    登录验证
    :return:
    """
    user = request.form.get('u')
    pasd = request.form.get('p')
    print(user, pasd)
    flag = sqllitDBHelper().check_login(user,pasd)
    print('-*-*-',flag)
    return jsonify(flag)

@app.route('/get_mounth_class_minutes', methods=['post'])
def get_mounth_class_minutes():
    uid = request.form.get('uid')
    date = request.form.get('date')
    print(uid, date)

@app.route('/getclass', methods=['post','get'])
def getclass():
    """
    登录成功后,根据uid查询出这个uid的所有课程数据
    :return:
    """
    uid = request.form.get('uid')
    if uid:
        print("收到uid:",uid)
        class_list = sqllitDBHelper().select_user_news(uid)
        return render_template('timeSheet.html', class_data_list=class_list,name=request.form.get('name'),uid=request.form.get('uid'))
    else:
        return render_template('index.html')

# @app.route('/getclassbyday', methods=['post'])
# def getclassbyday():
#     """
#     登录成功后,根据uid查询出这个uid的所有课程数据
#     :return:
#     """
#     uid = request.form.get('uid')
#     print("收到uid:",uid)
#     class_list = sqllitDBHelper().select_user_news(uid)
#     return jsonify(class_list)

@app.route('/deloneclass', methods=['post'])
def deloneclass():
    """
    登录成功后,根据itemid删除这条课程数据
    :return:
    """
    itemid = request.form.get('itemid')
    uid = request.form.get('uid')
    print("del收到itemid:",itemid)
    db = sqllitDBHelper()
    db.del_one_class(itemid)
    class_list = db.select_user_news(uid)
    return jsonify(class_list)

@app.route('/insert', methods=['post'])
def insert():
    """
    登录成功后,插入一条新数据
    :return:
    """
    start_end = request.form.get('start_end')
    start_time_list  = start_end.split(' - ')
    note = request.form.get('note')
    now_click_date = request.form.get('date')
    uid = request.form.get('uid')
    db = sqllitDBHelper()
    db.insert_data(uid, f'{now_click_date} {start_time_list[0]}', f'{now_click_date} {start_time_list[1]}', now_click_date, note)
    class_list = db.select_user_news(uid)
    return jsonify(class_list)

if __name__ == '__main__':
    # 启动服务 指定主机和端口
    app.run(host='0.0.0.0', port=19999, debug=True)
