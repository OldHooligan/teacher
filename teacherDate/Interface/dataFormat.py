#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021-04-06 23:44
# @Site    : 
# @File    : dataFormat.py
# @Software: PyCharm
import datetime

def sum_month_class_min(data):
    # data = {'2021-03-31': [[10, 1, '2021-03-31 22:04:13', '2021-03-31 18:35:00', '2021-03-31 17:15:00', '十中高一上选修课', '2021-03-31'], [11, 1, '2021-03-31 22:05:58', '2021-03-31 18:10:00', '2021-03-31 19:10:00', '十中高二 六人班', '2021-03-31'], [12, 1, '2021-03-31 22:08:08', '2021-03-31 20:15:00', '2021-03-31 21:15:00', '五中高二上课', '2021-03-31']],'2021-03-29': [[10, 1, '2021-03-31 22:04:13', '2021-03-31 16:35:00', '2021-03-31 17:15:00', '十中高一上选修课', '2021-03-31'], [11, 1, '2021-03-31 22:05:58', '2021-03-31 18:10:00', '2021-03-31 19:10:00', '十中高二 六人班', '2021-03-31'], [12, 1, '2021-03-31 22:08:08', '2021-03-31 20:15:00', '2021-03-31 21:15:00', '五中高二上课', '2021-03-31']]}
    da = data.values()
    new_list = []
    for item in da:
        for one_class in item:
            new_list.append([one_class[3], one_class[4]])
    month_min = 0
    if new_list:
            for item_date in new_list:
                try:
                    start_time = datetime.datetime.strptime(item_date[0], '%Y-%m-%d %H:%M:%S')
                    end_time = datetime.datetime.strptime(item_date[1], "%Y-%m-%d %H:%M:%S")
                    assert end_time > start_time, '开始时间大于结束时间'
                    secondsDiff = (end_time - start_time).seconds
                    # 两者相加得转换成分钟的时间差
                    minutesDiff = int(round(secondsDiff / 60, 0))
                    month_min += minutesDiff
                except Exception as e:
                    print(e)
            print(month_min)
            return month_min
    else:
        return 0

# sum_month_class_min()