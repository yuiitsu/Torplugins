# -*- coding:utf-8 -*-

"""
@author: delu
@file: cron_utils.py
@time: 17/7/4 18:05
"""
import time
from tools.date_utils import DateUtils


class CronUtils(object):
    count = 1

    def analyze(self, timestamp, cron_str):
        """
        处理cron表达式
        :param cron_str: 
        :return: 
        """
        x = time.localtime(timestamp)
        second = x.tm_sec
        minute = x.tm_min
        hour = x.tm_hour
        day = x.tm_mday
        month = x.tm_mon
        year = x.tm_year

        cron_list = cron_str.split(' ')

        second_str = cron_list[0]
        minute_str = cron_list[1]
        hour_str = cron_list[2]
        day_str = cron_list[3]
        month_str = cron_list[4]

        right_second, second_index, next_second_index, second_list, second_carry = self.process_base(second_str, 0, 59, second, 0)
        right_minute, minute_index, next_minute_index, minute_list, minute_cary = self.process_base(minute_str, 0, 59, minute, second_carry)
        right_hour, hour_index, next_hour_index, hour_list, hour_carry = self.process_base(hour_str, 0, 23, hour, minute_cary)
        right_day, day_index, next_day_index, day_list, day_cary = self.process_base(day_str, 1, 31, day, hour_carry)
        right_month, month_index, next_month_index, month_list, month_carry = self.process_base(month_str, 1, 12, month, day_cary)

        # left_days = (datetime.date(year, right_month, right_day) - datetime.date(year, month, day)).days
        # left_hour = right_hour - hour
        # left_minute = right_minute - minute
        # left_second = right_second - second
        # # 从小时到秒，挨个判断
        # if left_hour < 0:
        #     # 处理小时
        #     left_hour += 24
        # elif left_hour == 0 and left_minute < 0:
        #     left_minute += 60000
        # elif left_hour == 0 and left_minute == 0 and left_second < 0:
        #     if minute_str == '*':
        #         left_second += 60
        #     elif hour_str == '*':
        #         left_minute += 60
        #     elif day_str == '*':
        #         left_hour += 24
        #
        # left_timestamp = (((left_days * 24 + left_hour) * 60) + left_minute) * 60 + left_second
        if month_carry:
            right_month += month_carry
        date = ('{}-%s-%s %s:%s:%s' % tuple([('00'+str(i))[-2:] for
                                             i in (month, day, hour, minute, second)])).format(year)
        right_date = ('{}-%s-%s %s:%s:%s' % tuple([('00'+str(i))[-2:] for
                                             i in (right_month, right_day, right_hour, right_minute, right_second)])).\
            format(year)

        left_timestamp = DateUtils.str_to_time(right_date) - DateUtils.str_to_time(date)
        return left_timestamp

    def process_base(self, cron_str, min, max, current_time, carry=0):
        """
        解析只包含 , - * / 字符的表达式
        :param cron_str:
        :param carry: 进位
        :return: 
        """
        if '*' in cron_str or '?' in cron_str:
            str_list = [str(i) for i in range(int(min), int(max) + 1)]
        elif ',' in cron_str:
            str_list = cron_str.split(',')
        elif '-' in cron_str:
            str_list = cron_str.split('-')
            str_list = [str(i) for i in range(int(str_list[0]), int(str_list[1]) + 1)]
        elif '/' in cron_str:
            str_list = cron_str.split('/')
            str_list = [str(i) for i in range(int(str_list[0]), int(max) + 1, int(str_list[1]))]
        else:
            str_list = [cron_str]

        compare_time = current_time + carry
        if compare_time <= int(max):
            # 加上进位没有进位
            if str(compare_time) in str_list:
                index = str_list.index(str(compare_time))
                if len(str_list) > index + 1:
                    return compare_time, index, index + 1, str_list, 0
                else:
                    return compare_time, index, 0, str_list, 0
            else:
                for str_item in str_list:
                    if int(str_item) > compare_time:
                        index = str_list.index(str_item)
                        if len(str_list) > index + 1:
                            return int(str_item), index, index + 1, str_list, 0
                        else:
                            return int(str_item), index, 0, str_list, 0
                return int(str_list[0]), 0, -1, str_list, 1
        else:
            # 加上进位后有进位
            compare_time = compare_time - int(max) - 1
            if str(compare_time) in str_list:
                index = str_list.index(str(compare_time))
                if len(str_list) > index + 1:
                    return compare_time, index, index + 1, str_list, 1
                else:
                    return compare_time, index, 0, str_list, 1
            else:
                for str_item in str_list:
                    if int(str_item) > compare_time:
                        index = str_list.index(str_item)
                        if len(str_list) > index + 1:
                            return int(str_item), index, index + 1, str_list, 1
                        else:
                            return int(str_item), index, 0, str_list, 1
                return int(str_list[0]), 0, -1, str_list, 1


if __name__ == '__main__':
    cron_utils = CronUtils()
    current_time = int(time.time())
    # cron_str = '0 0 1 * *'
    cron_str = '0 0 10,17 * *'
    for i in range(20):
        left_time = cron_utils.analyze(current_time, cron_str)
        if left_time == 0:
            left_time += 1
            print DateUtils.format_time(current_time), left_time
            current_time += left_time
        else:
            current_time += left_time
            print DateUtils.format_time(current_time), left_time
            current_time += 1

