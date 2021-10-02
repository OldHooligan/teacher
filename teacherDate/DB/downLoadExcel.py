#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021-05-31 17:22
# @Site    : 
# @File    : downLoadExcel.py
# @Software: PyCharm
import os
import sqlite3
import xlwt
from XZGUtil.timeUtil import substract_Time_dil, str_totime, datetime_toChinStr, dil_str_toDatetime, datetime_toCustStr, \
    get_week_day
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
        style, style2 = self.get_style()
        sheet = workbook.add_sheet(self.sheet_name_xls)  # 在工作簿中新建一个表格

        first_col = sheet.col(0)  # xlwt中是行和列都是从0开始计算的
        sec_col = sheet.col(1)
        third_col = sheet.col(2)
        fourth_col = sheet.col(3)
        fifth_col = sheet.col(4)
        first_col.width = 256 * 20
        sec_col.width = 256 * 15
        third_col.width = 256 * 22
        fourth_col.width = 256 * 20
        fifth_col.width = 256 * 40

        for i in range(0, index):
            for j in range(0, len(self.value_title[i])):
                if i == 0:
                    sheet.write(i, j, self.value_title[i][j], style)  # 带样式的写入
                else:
                    sheet.write(i, j, self.value_title[i][j], style2)  # 像表格中写入数据（对应的行和列）
        workbook.save(f'./{self.book_name_xls}')  # 保存工作簿
        print("xls格式表格写入数据成功！")

    def get_style(self):
        style = xlwt.XFStyle()  # 初始化样式
        font = xlwt.Font()  # 为样式创建字体
        font.name = 'Times New Roman'
        font.bold = True  # 黑体
        font.height = 20 * 16  # 字体大小，11为字号，20为衡量单位
        style.font = font  # 设定样式

        pattern = xlwt.Pattern()  # Create the Pattern
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN  # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
        pattern.pattern_fore_colour = 5  # May be: 8 through 63. 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yell
        style.pattern = pattern  # Add Pattern to Style

        al = xlwt.Alignment()
        al.horz = 0x02  # 设置水平居中
        al.vert = 0x01  # 设置垂直居中
        style.alignment = al

        style2 = xlwt.XFStyle()  # 初始化样式
        font = xlwt.Font()  # 为样式创建字体
        font.name = 'Times New Roman'
        font.bold = True  # 黑体
        font.height = 20 * 11  # 字体大小，11为字号，20为衡量单位

        style2.font = font  # 设定样式
        style2.alignment = al
        return style, style2

class sqllitDBHelper():
    def __init__(self):
        # 连接到数据库
        # 如果数据库不存在的话，将会自动创建一个 数据库
        self.conn = sqlite3.connect(f"./date.db")
        self.value_title = [('日期', '星期', '上课时间', '课时（min）', "备注")]

    def select_data(self, uid, date_mounth):
        """查询上课记录"""
        cursor = self.conn.cursor()
        sql = f"select startTime,endTime,class_date,note from teachertiming where uid='{uid}' and class_date like '{date_mounth}%' order by note;"
        data = cursor.execute(sql)
        self.conn.commit()
        redeal_list = data.fetchall()
        redeal_list = [list(item) for item in redeal_list]
        for item in redeal_list:
            classdate = datetime_toChinStr(str_totime(item[2]))
            week = get_week_day(str_totime(item[2]))
            satrt_date = datetime_toCustStr(dil_str_toDatetime(item[0]), '%H:%M')
            end_date = datetime_toCustStr(dil_str_toDatetime(item[1]), '%H:%M')
            time_detail = substract_Time_dil(item[0], item[1]).get('min')
            vl = [classdate, week, f'{satrt_date}-{end_date}', time_detail, item[3]]
            self.value_title.append(vl)
            print(vl)
        create_excel(date_mounth, self.value_title).write_excel_xls()
        return redeal_list


if __name__ == '__main__':
    # print(timeUtil.substract_Time_detail('2021-05-01 09:00:00','2021-05-01 09:05:00'))
    user_id = input("请输入用户id:")
    mounth = input("请输入月份，例如:2021-05：")
    sqllitDBHelper().select_data(1,mounth)