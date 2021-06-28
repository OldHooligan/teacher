#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021-05-31 17:22
# @Site    : 
# @File    : downLoadExcel.py
# @Software: PyCharm
import os
import sqlite3
import datetime
import time
import xlrd
import xlwt
from xlutils.copy import copy
from XZGUtil import timeUtil
current_work_dir = os.path.dirname(__file__)
print(current_work_dir)

class create_excel():
    def __init__(self, date_mounth, value_title):
        self.book_name_xls = f'徐春秋-{date_mounth}.xls'
        self.sheet_name_xls = '课程日志'
        self.value_title = value_title

    def write_excel_xls(self):
        index = len(self.value_title)  # 获取需要写入数据的行数
        workbook = xlwt.Workbook()  # 新建一个工作簿
        sheet = workbook.add_sheet(self.sheet_name_xls)  # 在工作簿中新建一个表格
        for i in range(0, index):
            for j in range(0, len(self.value_title[i])):
                sheet.write(i, j, self.value_title[i][j])  # 像表格中写入数据（对应的行和列）
        workbook.save(f'./{self.book_name_xls}')  # 保存工作簿
        print("xls格式表格写入数据成功！")

class sqllitDBHelper():
    def __init__(self):
        # 连接到数据库
        # 如果数据库不存在的话，将会自动创建一个 数据库
        self.conn = sqlite3.connect(f"./date.db")
        self.value_title = [("上课时间", "下课时间", "上课日期", "备注", "课时/分钟")]

    def select_data(self, uid, date_mounth):
        """查询上课记录"""
        cursor = self.conn.cursor()
        sql = f"select startTime,endTime,class_date,note from teachertiming where uid='{uid}' and class_date like '{date_mounth}%' order by note;"
        data = cursor.execute(sql)
        self.conn.commit()
        redeal_list = data.fetchall()
        redeal_list = [list(item) for item in redeal_list]
        print(redeal_list)
        for item in redeal_list:
            time_detail = timeUtil.substract_Time_detail(item[0], item[1]).get('min')
            item.append(time_detail)
            self.value_title.append(item)
        create_excel(date_mounth,self.value_title).write_excel_xls()
        return redeal_list


if __name__ == '__main__':
    # print(timeUtil.substract_Time_detail('2021-05-01 09:00:00','2021-05-01 09:05:00'))
    user_id = input("请输入用户id:")
    mounth = input("请输入月份，例如:2021-05：")
    sqllitDBHelper().select_data(1,mounth)