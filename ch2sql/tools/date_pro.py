# -*- coding: utf-8 -*-
"""

Author: Rob

contributor:

This is a script file processing string about date.

这个版本目前只支持阿拉伯数字

"""
from datetime import date
import datetime
import calendar


# 获取当前季度

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
    str_in = str_in.strip()

    if (str_in.find('每月') != -1) | (str_in.find('每个月') != -1):
        byMon = True
        str_in = str_in.replace('每月', '')
        str_in = str_in.replace('每个月', '')

    if (str_in.find('每年') != -1) | (str_in.find('每一年') != -1):
        byYear = True
        str_in = str_in.replace('每年', '')
        str_in = str_in.replace('每一年', '')

    # 根据自然语言进行对应的处理
    # 特殊情况处理
    if str_in == '':
        return begin, end, isRange, byMon, byYear

    elif str_in.find('昨天') != -1:
        begin = today - datetime.timedelta(1)
    elif str_in.find('前天') != -1:
        begin = today - datetime.timedelta(2)

    elif str_in.find('天前') != -1:
        days = int(str_in[0:str_in.find('天前')])
        begin = today - datetime.timedelta(days)


    # 最近类型日期处理
    elif str_in.find('最近') != -1:
        isRange = True

        str_begin = str_in.find('最近') + 2

        if str_in.find('年') != -1:
            year = today.year - int(str_in[str_begin: str_in.find('年')])
            begin = begin.replace(year, 1, 1)

        elif str_in.find('个') != -1:

            str_end = str_in.find('个')
            number = int(str_in[str_begin: str_end])

            if str_in.find('季度') != -1:

                season = (today.month - 1) // 3 - number
                year = today.year
                month = season * 3 + 1
                while month < 0:
                    year -= 1
                    month += 12

                begin = begin.replace(year, month, 1)

            elif str_in.find('月') != -1:

                year = today.year
                month = today.month - number
                while month < 0:
                    year -= 1
                    month += 12
                begin = begin.replace(year, month, 1)

        elif str_in.find('季度') != -1:

            season = (today.month - 1) // 3 - int(str_in[str_begin: str_in.find('季度')])
            year = today.year
            month = season * 3 + 1
            while month < 0:
                year -= 1
                month += 12

            begin = begin.replace(year, month, 1)


        elif str_in.find('月') != -1:
            year = today.year
            month = today.month - int(str_in[str_begin: str_in.find('月')])
            while month < 0:
                year -= 1
                month += 12
            begin = begin.replace(year, month, 1)

        elif str_in.find('天') != -1:
            days = int(str_in[str_begin: str_in.find('天')])
            begin = today - datetime.timedelta(days)

            # 年月日类型日期处理
    elif str_in.find('年') != -1:

        isRange = True

        # 年的特殊情况处理
        if (str_in.find('今年') != -1) | (str_in.find('该年') != -1) | (str_in.find('本年') != -1) | (
                    str_in.find('这年') != -1) | (str_in.find('这一年')):
            year = today.year

        elif str_in.find('去年') != -1:
            year = today.year - 1

        elif (str_in.find('前年') != -1) | (str_in.find('前一年') != -1):
            year = today.year - 2

        # 年的通用情况处理
        else:
            year = int(str_in[0:str_in.find('年')])

        if str_in.find('月') == -1:

            begin = today.replace(year, 1, 1)
            if year != today.year:
                end = today.replace(year, 12, 31)

        else:

            month = int(str_in[str_in.find('年') + 1: str_in.find('月')])

            if (str_in.find('日') == -1) & (str_in.find('号') == -1):

                day = calendar.monthrange(year, month)[1]

                begin = today.replace(year, month, 1)
                end = today.replace(year, month, day)

            else:

                if str_in.find('日') != -1:
                    day = int(str_in[str_in.find('月') + 1: str_in.find('日')])
                elif str_in.find('号') != -1:
                    day = int(str_in[str_in.find('月') + 1: str_in.find('号')])

                isRange = False
                begin = begin.replace(year, month, day)

                # 没有年的特殊情况处理
    elif (str_in.find('这') != -1) | (str_in.find('本') != -1):

        isRange = True

        if str_in.find('月') != -1:
            year = today.year
            month = today.month

            begin = begin.replace(year, month, 1)

        if str_in.find('季度') != -1:
            season = (today.month - 1) // 3
            year = today.year
            month = season * 3 + 1

            begin = begin.replace(year, month, 1)


    elif str_in.find('上') != -1:

        isRange = True

        if str_in.find('月') != -1:

            year = today.year
            month = today.month - 1

            while month < 0:
                year -= 1
                month += 12

            day = calendar.monthrange(year, month)[1]

            begin = begin.replace(year, month, 1)
            end = end.replace(year, month, day)

        if str_in.find('季度') != -1:
            season = (today.month - 1) // 3 - 1
            year = today.year
            month = season * 3 + 1
            while month < 0:
                year -= 1
                month += 12

            begin = begin.replace(year, month, 1)

            month += 2
            while month > 12:
                year += 1
                month -= 12

            day = calendar.monthrange(year, month)[1]

            end = end.replace(year, month, day)


    elif str_in.find('前') != -1:
        isRange = True

        if str_in.find('月') != -1:
            year = today.year
            month = today.month - 2
            while month < 0:
                year -= 1
                month += 12

            day = calendar.monthrange(year, month)[1]

            begin = begin.replace(year, month, 1)
            end = end.replace(year, month, day)

        if str_in.find('季度') != -1:
            season = (today.month - 1) // 3 - 2
            year = today.year
            month = season * 3 + 1
            while month < 0:
                year -= 1
                month += 12

            begin = begin.replace(year, month, 1)

            month += 2
            while month > 12:
                year += 1
                month -= 12

            day = calendar.monthrange(year, month)[1]

            end = end.replace(year, month, day)


    # 没有年的情况处理
    elif str_in.find('月') != -1:

        isRange = True

        year = today.year
        month = int(str_in[0:str_in.find('月')])
        day = calendar.monthrange(year, month)[1]

        begin = today.replace(year, month, 1)
        end = today.replace(year, month, day)


    # 没有月的情况处理
    elif (str_in.find('日') != -1) | (str_in.find('号') != -1):

        isRange = False

        year = today.year
        month = today.month

        if str_in.find('日') != -1:
            day = int(str_in[0:str_in.find('日')])

        elif str_in.find('号') != -1:
            day = int(str_in[0:str_in.find('号')])

        begin = begin.replace(year, month, day)

    return begin, end, isRange, byMon, byYear


if __name__ == '__main__':
    str_in = '下个月'

    begin, end, isRange, byMon, byYear = ch2date(str_in)

    print(begin)
    print(end)
    print(isRange)
    print(byMon)
    print(byYear)
