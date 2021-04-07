#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021-02-22 18:05
# @Site    : 
# @File    : JJSqlite.py
# @Software: PyCharm
# 导入数据库驱动
import os
import sqlite3
import datetime
import time

from XZGUtil import timeUtil

current_work_dir = os.path.dirname(__file__)
print(current_work_dir)


class sqllitDBHelper():
    def __init__(self):
        # 连接到数据库
        # 如果数据库不存在的话，将会自动创建一个 数据库
        self.conn = sqlite3.connect(f"{current_work_dir}/date.db")

    def create_table(self):
        """教师上课时间表"""
        cursor = self.conn.cursor()
        sql = """CREATE TABLE teachertiming (
                  id INTEGER PRIMARY KEY,
                  uid int(32),
                  create_date timestamp,
                  startTime timestamp,
                  endTime timestamp,
                  note text,
                  class_date timestamp
                )"""
        cursor.execute(sql)
        # 关闭游标：
        cursor.close()
        # 提交事物
        self.conn.commit()

    def create_user_table(self):
        # 教师表
        cursor = self.conn.cursor()
        sql = """CREATE TABLE teacher(
                  id INTEGER PRIMARY KEY,
                  uid int(32),
                  name varchar(64),
                  passwd varchar(64),
                  create_date timestamp)"""
        cursor.execute(sql)
        # 关闭游标：
        cursor.close()
        # 提交事物
        self.conn.commit()

    def insert_user_data(self, uid, user, passwd):
        """插入一条教师账户"""
        user = user.replace('"', '‘').replace("'", '‘')
        passwd = passwd.replace('"', '‘').replace("'", '‘')
        cursor = self.conn.cursor()
        d_now = timeUtil.datetime_toString_detail(datetime.datetime.now())
        sql = f"insert into teacher(uid,name,passwd,create_date) values ({uid},'{user}','{passwd}','{d_now}');"
        print(sql)
        cursor.execute(sql)
        # 提交事物
        self.conn.commit()

    def check_login(self, user, passwd):
        """验证账户"""
        user = user.replace('"','‘').replace("'",'‘')
        passwd = passwd.replace('"', '‘').replace("'", '‘')
        cursor = self.conn.cursor()
        sql = f"select * from teacher where name='{user}';"
        data = cursor.execute(sql)
        self.conn.commit()
        data = data.fetchall()
        print(data)
        try:
            pw = data[0][3]
            if passwd == pw:
                return {'state':True,'uid':data[0][1],'name':data[0][2]}
            else:
                return {'state':False}
        except:
            return {'state':False}

    def insert_data(self, uid, startTime, endTime, class_date, note=None):
        # 插入一条上课记录
        if startTime > endTime:
            print('开始时间大于结束时间')
            return
        note = self.sql_filter(note)
        print(uid, startTime, endTime, class_date, note)
        cursor = self.conn.cursor()
        d_now = timeUtil.datetime_toString_detail(datetime.datetime.now())
        sql = f"insert into teachertiming(uid,create_date,startTime,endTime,class_date,note) values ({uid},'{d_now}','{startTime}','{endTime}','{class_date}','{note}');"
        print(sql)
        cursor.execute(sql)
        # 提交事物
        self.conn.commit()

    def sql_filter(self,note):
        note = note.replace(",", "，")
        dirty_stuff = ["\"", "\\", "/", "*", "'", "=", "-", "#", ";", "<", ">", "+", "%", "$", "(", ")", "%", "@", "!"]
        for stuff in dirty_stuff:
            str = note.replace(stuff, "")
        return note

    def select_user_news(self, uid, date_mounth="202"):
        """查询上课记录"""
        cursor = self.conn.cursor()
        sql = f"select * from teachertiming where uid='{uid}' and class_date like '{date_mounth}%';"
        data = cursor.execute(sql)
        self.conn.commit()
        li = data.fetchall()
        redeal_list = self.create_class_data(li)
        return redeal_list

    def del_one_class(self, itemid):
        """查询上课记录"""
        cursor = self.conn.cursor()
        sql = f"DELETE  from teachertiming where id='{itemid}';"
        cursor.execute(sql)
        self.conn.commit()
        print(f'itemid:{itemid}删除成功！')

    def create_class_data(self,data_list):
        """将查询出来的每日课程结果进行按天归类"""
        redeal_list = {}
        for item in data_list:
            key = f'{item[-1].split(" ")[0]}'
            if f'{key}' not in redeal_list.keys():
                redeal_list[f"{key}"] = [list(item)]
            else:
                redeal_list.get(key).append(list(item))
        print(redeal_list)
        return redeal_list

    def close_db(self):
        # 关闭连接
        self.conn.close()

    def test(self, code):
        cursor = self.conn.cursor()
        sql = f'select * from code_news where code="{code}"'
        data = cursor.execute(sql)
        self.conn.commit()
        li = data.fetchall()
        print(li)


if __name__ == '__main__':
    # sqllitDBHelper().create_table()
    # sqllitDBHelper().create_user_table()
    # sqllitDBHelper().insert_user_data(66666,'zhang','sssss')
    # sqllitDBHelper().check_login('1', '1')
    # sqllitDBHelper().insert_data(1, datetime.datetime.now(), datetime.datetime.now(), datetime.datetime.now())
    sqllitDBHelper().select_user_news(66666, '2021-04')
