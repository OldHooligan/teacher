#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021-02-19 10:31
# @Site    :
# @File    : JJInterface.py
# @Software: PyCharm
import os
import sys
from urllib.parse import quote
curPath = os.path.abspath(os.path.dirname(__file__))
print(curPath)
rootPath = os.path.split(curPath)[0] + '/'
print(rootPath)
sys.path.append(os.path.split(rootPath)[0])
from flask import Flask, request, jsonify, render_template, make_response, send_from_directory, send_file
# 创建一个服务
from DB.JJSqlite import sqllitDBHelper
from Interface.dataFormat import sum_month_class_min
app = Flask(__name__, template_folder='../templates', static_folder='../static')
from DB.downLoadExcel import sqlDBHelper
dl = sqlDBHelper()

# 创建一个接口 指定路由和请求方法 定义处理请求的函数
@app.route('/login', methods=['GET'])
def everything():
    """
    请求登录页
    :return:
    """
    return render_template('index.html')

@app.route('/', methods=['GET'])
def login():
    """
    请求登录页
    :return:
    """
    return render_template('index.html')

@app.route('/<path>')
def today(path):
    try:
        base_dir = os.path.dirname(__file__)
        resp = make_response(open(os.path.join(base_dir, path)).read())
        resp.headers["Content-type"] = "text/plan;charset=UTF-8"
        return resp
    except:
        re = jsonify({"msg": False})
        return 

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
    print('-*-*-', flag)
    return jsonify(flag)

@app.route('/get_mounth_class_minutes', methods=['post'])
def get_mounth_class_minutes():
    """
    获取月度总共分钟数
    :return:
    """
    uid = request.form.get('uid')
    curYear = request.form.get('curYear')
    curMonth = request.form.get('curMonth')
    if len(curMonth) < 2:
        curMonth = f'0{curMonth}'
    class_list = sqllitDBHelper().select_user_news(uid, curYear+'-'+curMonth)
    min = sum_month_class_min(class_list)
    return jsonify({'min':min})

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
    start_time_list = start_end.split(' - ')
    note = request.form.get('note')
    now_click_date = request.form.get('date')
    uid = request.form.get('uid')
    db = sqllitDBHelper()
    db.insert_data(uid, f'{now_click_date} {start_time_list[0]}', f'{now_click_date} {start_time_list[1]}', now_click_date, note)
    class_list = db.select_user_news(uid)
    return jsonify(class_list)

@app.route("/downloadxls", methods=['get'])
def download_file():
    # 需要知道2个参数, 第1个参数是本地目录的path, 第2个参数是文件名(带扩展名)
    uid = request.args.get('uid')
    date_mounth = request.args.get('date_mounth')[:-3]
    directory, filename = dl.select_data(uid, date_mounth)
    print('*', directory, filename)
    download_file_name = quote(filename)
    rv = send_file(directory, as_attachment=True, attachment_filename=download_file_name)
    rv.headers['Content-Disposition'] = "; filename*=utf-8''%s" % (download_file_name)
    return rv

if __name__ == '__main__':
    # 启动服务 指定主机和端口
    app.run(host='0.0.0.0', port=19999, debug=True)
