# -*- coding:utf-8 -*-

"""
@author: delu
@file: schedule_utils.py
@time: 17/5/2 下午4:11
"""
from tools.my_scheduler import MyScheduler
from source.system_constants import SystemConstants
import MySQLdb
from DBUtils.PooledDB import PooledDB
from source.properties import Properties
import time

properties = Properties()


class ScheduleUtils(object):
    scheduler = None
    if not scheduler:
        pool = PooledDB(
            creator=MySQLdb,
            mincached=5,
            maxcached=20,
            host=properties.get('jdbc', 'DB_HOST'),
            user=properties.get('jdbc', 'DB_USER'),
            passwd=properties.get('jdbc', 'DB_PASS'),
            db=properties.get('jdbc', 'DB_BASE'),
            port=int(properties.get('jdbc', 'DB_PORT')),
            use_unicode=1,
            charset='utf8'
        )
        job_stores = {
            'pool': pool
        }
        scheduler = MyScheduler(job_stores=job_stores)
        scheduler.start()
        scheduler.add_job('plugins.schedule.order.service', 'do_task', {}, 'order_task', limit_time=24 * 60 * 60,
                          repeat_count=-1, cron='0 0 1 * *')

    @staticmethod
    def add_job(service_path, method, params={}, job_id='', group='default', start_time='', limit_time=0,
                repeat_count=0, cron=''):
        """
        添加任务
        :param params: 
        :return: 
        """
        try:
            ScheduleUtils.scheduler.add_job(service_path, method, params, job_id, group, start_time, limit_time,
                                            repeat_count, cron)
            return SystemConstants.SUCCESS
        except Exception, e:
            print Exception, ':', e
            return SystemConstants.SCHEDULE_ADD_JOB_ERROR

    @staticmethod
    def remove_job(job_id):
        """
        移除任务
        :param job_id: 
        :return: 
        """
        try:
            ScheduleUtils.scheduler.remove_job(job_id)
            return SystemConstants.SUCCESS
        except Exception, e:
            print Exception, ':', e
            return SystemConstants.SCHEDULE_REMOVE_JOB_ERROR

    def test(self, params):
        print params['name']


if __name__ == '__main__':
    params = {
        'name': 'delu',
        'hello': 'world'
    }
    ScheduleUtils.add_job('user.service.user_service', 'test', params=params, job_id='test1',
                          start_time='2017-06-07 10:39:10')

    while True:
        print 'wait...'
        time.sleep(1)
