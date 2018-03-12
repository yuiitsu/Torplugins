# -*- coding:utf-8 -*-

"""
@author: delu
@file: my_scheduler.py
@time: 17/5/23 下午2:17
自定义任务管理类
"""
import pickle
import threading
import time
import MySQLdb
from source.service_manager import ServiceManager
from tools.cron_utils import CronUtils
from tools.date_utils import DateUtils


class MyScheduler(object):
    job_stores = None
    pool = None
    func = None
    job_id_list = {}
    cron_utils = CronUtils()

    def __init__(self, job_stores=None):
        """
        初始化
        :param job_stores: 用于存储任务到数据源
        """
        self.func = getattr(self, 'do_work')
        self.job_stores = job_stores
        if job_stores:
            self.pool = job_stores['pool']

    def add_job(self, service_path, method, params={}, job_id='',
                group='default', start_time='', limit_time=0, repeat_count=0, cron=''):
        """
        添加定时任务
        :param job: 
        :return: 
        """
        if job_id in self.job_id_list:
            print Exception('job_id {%s} 已存在' % job_id)
            return
        if self.job_stores and not job_id:
            print Exception('如果想序列化至数据源，则job_id非空')
            return
        try:
            left_time = 0
            if cron:
                current_timestamp = int(time.time())
                # 如果传入cron表达式，则以cron表达式为主
                left_time = self.cron_utils.analyze(current_timestamp, cron)
                start_time = DateUtils.format_time(current_timestamp + left_time)
            if start_time and not limit_time and not repeat_count:
                """
                单次任务
                """
                start_timestamp = int(time.mktime(time.strptime(start_time, '%Y-%m-%d %H:%M:%S')))
                current_timestamp = int(time.time())
                if current_timestamp > start_timestamp:
                    print '启动时间小于当前时间, 立刻启动'
                    left_time = 0
                else:
                    left_time = start_timestamp - current_timestamp
                type = 'one'
            elif limit_time >= 0 and repeat_count > 0:
                """
                多次任务，但不是无限循环
                """
                type = 'many'
            elif repeat_count < 0:
                """
                无限循环
                """
                type = 'circle'
            job_params = {
                'params': params,
                'service_path': service_path,
                'method': method,
                'left_time': left_time,
                'limit_time': limit_time,
                'repeat_count': repeat_count,
                'type': type,
                'job_id': job_id,
                'group_name': group,
                'start_time': start_time,
                'cron': cron
            }
            thread = threading.Thread(target=self.func, args=[job_params])
            thread.start()
            self.job_id_list[job_id] = 1
            # 将任务存储至数据库
            if self.job_stores:
                self.save_job(job_params)
            print '定时任务启动'
            print job_params
            return thread
        except Exception, e:
            print Exception("启动定时任务失败")
            return

    def do_work(self, job_params={}):
        """
        启动任务
        :param job_params: 
        :return: 
        """
        if job_params['type'] == 'one':
            # 执行单次任务
            time.sleep(job_params['left_time'])
            # 将执行时间加入任务参数中
            if isinstance(job_params['params'], dict) and 'notify_start_time' not in job_params['params']:
                job_params['params']['notify_start_time'] = job_params['start_time']
            ServiceManager.do_service(job_params['service_path'], job_params['method'], job_params['params'], 'v1')
            if self.job_stores and job_params['job_id']:
                # 从数据库中移除任务
                conn = self.pool.connection()
                cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
                sql = 'delete from tbl_cfg_schedule_job where job_id = %s'
                cursor.execute(sql, (job_params['job_id'],))
                conn.commit()
        elif job_params['type'] == 'many':
            # 执行多次任务
            repeat_count = job_params['repeat_count']
            while True:
                ServiceManager.do_service(job_params['service_path'], job_params['method'], job_params['params'], 'v1')
                time.sleep(job_params['limit_time'])
                if repeat_count:
                    repeat_count -= 1
                else:
                    break
            if self.job_stores and job_params['job_id']:
                # 从数据库中移除任务
                conn = self.pool.connection()
                cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
                sql = 'delete from tbl_cfg_schedule_job where job_id = %s'
                cursor.execute(sql, (job_params['job_id'],))
                conn.commit()
        elif job_params['type'] == 'circle':
            # 无限循环
            print job_params['job_id'], 'sleep', job_params['left_time'], time.localtime(time.time())
            time.sleep(job_params['left_time'])
            while True:
                ServiceManager.do_service(job_params['service_path'], job_params['method'], job_params['params'], 'v1')
                current_timestamp = int(time.time())
                left_time = self.cron_utils.analyze(current_timestamp, job_params['cron'])
                while left_time == 0:
                    # 防止多次执行
                    time.sleep(0.1)
                    current_timestamp = int(time.time())
                    left_time = self.cron_utils.analyze(current_timestamp, job_params['cron'])
                print job_params['job_id'], 'sleep', left_time, time.localtime(current_timestamp)
                time.sleep(left_time)

                # print 'wait 600'
                # time.sleep(600)
                # time.sleep(job_params['limit_time'])
        self.job_id_list.pop(job_params['job_id'])

    def save_job(self, job_params):
        """
        将任务保存至数据库
        :param job_params: 
        :return: 
        """
        conn = self.pool.connection()
        cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        try:
            create_table_sql = "CREATE TABLE if not EXISTS " \
                               "tbl_cfg_schedule_job (" \
                               "job_id varchar(100) NOT NULL default '' COMMENT '任务编号(买家定义)', " \
                               "group_name varchar(100) not NULL default '' comment '任务分组编号', " \
                               "start_time varchar(30) NOT NULL COMMENT '开始时间', " \
                               "limit_time int(11) not null DEFAULT 0 comment '间隔时间(以秒为单位)', " \
                               "repeat_count int(11) not null DEFAULT 0 comment '重复次数(-1 为无限循环)', " \
                               "job_data blob not null comment '任务序列化数据', " \
                               "create_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间', " \
                               "PRIMARY KEY (job_id))" \
                               " ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='定时任务job表'"
            cursor.execute(create_table_sql)

            job_sql = 'insert into tbl_cfg_schedule_job(job_id, group_name, start_time, limit_time, repeat_count,' \
                      'job_data, cron) values(%s, %s, %s, %s, %s, %s, %s)'
            cursor.execute(job_sql, (job_params['job_id'], job_params['group_name'], job_params['start_time'],
                                     job_params['limit_time'], job_params['repeat_count'], pickle.dumps(job_params),
                                     job_params['cron']))
            conn.commit()
        except Exception, e:
            print Exception, ':', e
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

    def start(self):
        """
        从数据库中读取数据，初始化定时任务
        :return: 
        ：update: wsy 2017/8/11
        """
        if self.job_stores:
            conn = self.pool.connection()
            cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            # 查找出数据库中现存的所有任务
            sql = 'SELECT * FROM tbl_cfg_schedule_job ORDER BY start_time DESC'  # where start_time > now() or (repeat_count = -1)
            cursor.execute(sql)
            job_list = cursor.fetchall()
            for job in job_list:
                try:
                    job_params = pickle.loads(job['job_data'])
                    if job_params['cron']:
                        current_timestamp = int(time.time())
                        job_params['left_time'] = self.cron_utils.analyze(current_timestamp, job_params['cron'])
                        job_params['start_time'] = DateUtils.format_time(current_timestamp + job_params['left_time'])
                    if job_params['type'] == 'one':
                        """
                        单次任务
                        """
                        start_timestamp = int(time.mktime(time.strptime(job['start_time'], '%Y-%m-%d %H:%M:%S')))
                        current_timestamp = int(time.time())
                        if current_timestamp > start_timestamp:
                            left_time = 0
                            print ('启动时间小于当前时间,立刻执行')
                        else:
                            left_time = start_timestamp - current_timestamp
                        job_params['left_time'] = left_time
                    elif job_params['type'] == 'many':
                        pass
                    elif job_params['type'] == 'circle':
                        pass
                    thread = threading.Thread(target=self.func, args=[job_params])
                    thread.start()
                    self.job_id_list[job_params['job_id']] = 1
                    print '定时任务启动'
                    print job_params
                except Exception, e:
                    print Exception, ':', e

    def remove_job(self, job_params):
        """
        从数据库中移除任务数据
        :return:
        :create:wsy 2017/08/09
        """
        if self.job_stores and job_params['job_id'] and job_params['job_id'] in self.job_id_list:
            # 从数据库中移除任务
            self.job_id_list.pop(job_params['job_id'])
            conn = self.pool.connection()
            cursor = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            sql = 'delete from tbl_cfg_schedule_job where job_id = %s'
            cursor.execute(sql, (job_params['job_id'],))
            conn.commit()
