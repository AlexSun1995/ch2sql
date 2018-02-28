# -*- coding: utf-8 -*-
"""

Author: Rob

contributor:

This is a script file processing string about date.

"""
from datetime import date
import datetime
import calendar


# 将字符日期转换为数字日期
def ch2date(str_in):
    # 记录返回结果是否按月
    byMon = False

    # 记录返回结果是否按年
    byYear = False

    # return a time object including today's date to variable today
    today = date.today()

    # 记录终止日期，默认中止日期为当前日期
    end = today

    # initialise beginning date, default to be today
    begin = today

    # judge the query date type, if isRange equals True, ignore 'end',
    # else both are valid
    isRange = False

    # 预处理
    if str_in.find('每月') != -1 | str_in.find('每个月') != -1:
        byMon = True
        str_in.replace('每月', '')
        str_in.replace('每个月', '')

    if str_in.find('每年') != -1 | str_in.find('每一年') != -1:
        byYear = True
        str_in.replace('每年', '')
        str_in.replace('每一年', '')

    # 根据自然语言进行对应的处理
    # 特殊情况处理
    if str_in.find('昨天') != -1:
        begin = today - datetime.timedelta(1)
    elif str_in.find('前天') != -1:
        begin = today - datetime.timedelta(2)

    elif str_in.find('今年') != -1:
        isRange = True
        begin = begin.replace(today.year, 1, 1)
    elif str_in.find('去年') != -1:
        isRange = True
        year = today.year - 1
        begin = begin.replace(year, 1, 1)
        end = end.replace(year, 12, 31)

    elif str_in.find('这') != -1:

        isRange = True

        if str_in.find('月') != -1:
            year = today.year
            month = today.month

            begin = begin.replace(year, month, 1)

        if str_in.find('季度') != -1:
            pass
        if str_in.find('年') != -1:
            year = today.year
            begin = begin.replace(year, 1, 1)

    elif str_in.find('上') != -1:

        isRange = True

        if str_in.find('月') != -1:
            year = today.year
            month = today.month - 1
            day = calendar.monthrange(year, month)

            begin = begin.replace(year, month, 1)
            end = end.replace(year, month, day)

        if str_in.find('季度') != -1:

        if str_in.find('年') != -1:
            year = today.year - 1
            begin = begin.replace(year, 1, 1)
            end = end.replace(year, 12, 31)


    elif str_in.find('前') != -1:
        isRange = True

        if str_in.find('月') != -1:
            year = today.year
            month = today.month - 2
            day = calendar.monthrange(year, month)

            begin = begin.replace(year, month, 1)
            end = end.replace(year, month, day)

        if str_in.find('季度') != -1:

        if str_in.find('年') != -1:
            year = today.year - 2
            begin = begin.replace(year, 1, 1)
            end = end.replace(year, 12, 31)

    # 单点日期处理
    elif str_in.find('日') != -1 | str_in.find('号') != -1:

        if str_in.find('月') != -1:

            if str_in.find('年') != -1:

                year = str_in[0: str_in.find("年")]
            else:
                year = today.year

            month = str_in[str_in.find('年') + 1: str_in.find('月')]
        else:
            month = today.month

        if str_in.find('日') != -1:
            day = str_in[str_in.find('月') + 1: str_in.find('日')]
        if str_in.find('号') != -1:
            day = str_in[str_in.find('月') + 1: str_in.find('号')]

        begin = today.replace(int(year), int(month), int(day))

    elif str_in.find('天前') != -1:
        days = int(str_in[0:str_in.find('天前')])
        begin = today - datetime.timedelta(days)


        # 范围日期处理
    else:
        isRange = True

        # 最近类型的日期
        if str_in.find('最近') != -1:

            str_begin = str_in.find('最近') + 2

            if str_in.find('年') != -1:
                year = today.year - int(str_in[str_begin: str_in.find('年')])
                begin = begin.replace(year, 1, 1)

            elif str_in.find('个月') != -1:
                month = today.month - int(str_in[str_begin: str_in.find('个月')])
                begin = begin.replace(today.year, month, 1)

            elif str_in.find('月') != -1:
                month = today.month - int(str_in[str_begin: str_in.find('月')])
                begin = begin.replace(today.year, month, 1)

            elif str_in.find('天') != -1:
                day = today.day - int(str_in[str_begin: str_in.find('天')])
                begin = today.replace(today.year, today.month, day)


        elif str_in.find('月') != -1:

            year = today.year
            month = int(str_in[0:str_in.find('月')])
            day = calendar.monthrange(year, month)

            begin = today.replace(year, month, 1)
            end = today.replace(year, month, day)

        elif str_in.find('年') != -1:
            year = int(str_in[0:str_in.find('年')])
            begin = today.replace(year, 1, 1)
            end = today.replace(year, 12, 31)

    return begin, end, isRange, byMon, byYear