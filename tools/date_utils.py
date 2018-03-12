# -*- coding:utf-8 -*-

"""
@author: delu
@file: date_utils.py
@time: 17/5/2 下午5:44
"""
import time


class DateUtils(object):

    YYYY_MM_DD = '%Y-%m-%d'
    YYYY_MM_DD_HH_MM_SS = '%Y-%m-%d %H:%M:%S'

    @staticmethod
    def format_time(timestamp, time_format='%Y-%m-%d %H:%M:%S'):
        """
        将时间戳格式化为时间字符串
        :param timestamp: int 时间戳 
        :param time_format: string 时间格式，默认为 '%Y-%m-%d %H:%M:%S'
        :return: 
        """
        return time.strftime(time_format, time.localtime(timestamp))

    @staticmethod
    def time_now(time_format='%Y-%m-%d %H:%M:%S'):
        """
        获取当前时间，yyyy-mm-dd H:M:S
        :return: 
        """
        return DateUtils.format_time(time.time(), time_format)

    @staticmethod
    def str_to_time(date, format_date="%Y-%m-%d %H:%M:%S"):
        """ 
        将日期字符串转为时间戳
        :param date: string 时间字符串，如：2017-04-28 10:00:00
        :param format_date: 时间格式，默认为 '%Y-%m-%d %H:%M:%S'
        """
        try:
            time_array = time.strptime(date, format_date)
            return int(str(time.mktime(time_array)).split('.')[0])
        except Exception, e:
            print e
            return 0

    @staticmethod
    def time_to_str(date_time, format_date='%Y-%m-%d %H:%M:%S'):
        """
        将日期转为字符串
        :param date_time: 
        :param format_date: 
        :return: 
        """
        return date_time.strftime(format_date)

    @staticmethod
    def add_minute(date_str, format_date='%Y-%m-%d %H:%M:%S', minutes=0):
        """
        增加分钟
        :param date_str: 日期字符串
        :param format_date:
        :param minutes: 增加的分钟
        :return: 
        """
        time_array = time.strptime(date_str, format_date)
        mytime = str(time.mktime(time_array)).split('.')[0]
        mytime = int(mytime) + (60 * minutes)
        return time.strftime(format_date, time.localtime(mytime))

if __name__ == '__main__':
    print DateUtils.add_minute(DateUtils.time_now(DateUtils.YYYY_MM_DD) + ' 00:00:00', minutes=25 * 60, type='str')


