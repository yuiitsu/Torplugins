# -*- coding:utf-8 -*-

"""
@author: delu
@file: task_manager.py
@time: 17/6/5 15:55
"""
import json
import sys; sys.path.append("../")
import time
import threadpool

import conf.config as config
from constants.cachekey_predix import CacheKeyPredix as cachekey
from source.redisbase import RedisBase
from source.service_manager import ServiceManager
from tools.schedule_utils import ScheduleUtils
from tools.date_json_encoder import CJsonEncoder
from source.properties import Properties
from source.model import ModelBase
from tools.date_utils import DateUtils
import traceback
from tools.logs import Logs

properties = Properties()

pool_size = 3
try:
    pool_size = int(properties.get('task', 'POOL_NUM'))
except Exception, e:
    print e

redis = RedisBase()
task_redis = redis.get_conn()
error_redis = redis.get_conn()
cache_key = cachekey.TASK_DATA_LIST
error_cache_key = cachekey.ERROR_TASK_DATA_LIST
pool = threadpool.ThreadPool(pool_size)
service_manager = ServiceManager()
config = config
logger = Logs().get_logger()


def update_task(last_id):
    """
    更新任务完成状态
    :param last_id:
    :return:
    """
    model = ModelBase()
    fields = [
        'is_complete = 1'
    ]
    condition = ' id = %s '
    value_tuple = (last_id,)
    result = model.update('tbl_task_job_logs', {
        model.sql_constants.FIELDS: fields,
        model.sql_constants.CONDITION: condition
    }, value_tuple)

    return result


def save_task(package_path, data):
    """
    任务入库
    :param package_path:
    :param data:
    :return:
    """
    model = ModelBase()
    # key
    key = 'package_path, data'
    # val
    val = '%s,%s'
    # value
    value_tuple = (package_path, data)
    result = model.insert('tbl_task_job_logs', {
        model.sql_constants.KEY: key,
        model.sql_constants.VAL: val
    }, value_tuple)
    return result['last_id']


def do_task(service_path, method, params, last_id):
    """
    处理任务
    :param service_path: 
    :param method: 
    :param params: 
    :param last_id:
    :return:
    """
    count = 0
    while True:
        try:
            result = service_manager.do_local_service(service_path, method, params, config.CONF['version'])
            if result is not None and result['code'] == 0:
                # 更新完成状态
                update_task(last_id)
            break
        except Exception, e:
            logger.error('任务异常 service: %s, method: %s, params: %s, traceback: %s ' % (service_path, method, params,
                                                                                        traceback.format_exc()))
        count += 1
        if count >= 3:
            # 连续失败3次，则进入失败队列
            task_data = {
                'service_path': service_path,
                'method': method,
                'params': params
            }
            logger.info('连续失败了3次，进入失败队列')
            error_redis.lpush(error_cache_key, json.dumps(task_data, cls=CJsonEncoder))
            break
        # 每隔1秒，重试一次
        time.sleep(0.1)


def run(params):
    """
    监控任务列表
    :return: 
    """
    while True:
        # 读取任务
        task_data_str = ''
        try:
            task_data_str = task_redis.rpop(cache_key)
            if task_data_str:
                logger.info('处理异步任务 %s' % task_data_str)
                task_data = json.loads(task_data_str)
                # 任务入库
                last_id = save_task(task_data['service_path'], task_data_str)
                # 执行任务
                do_task(task_data['service_path'], task_data['method'], task_data['params'], last_id)
        except Exception, e:
            logger.error('异步任务异常 %s, %s' % (task_data_str, e))

        time.sleep(0.1)

    # try:
    #     task_data = task_redis.rpop(cache_key)
    #     if task_data:
    #         print '处理异步任务'
    #         print task_data
    #         task_data = json.loads(task_data)
    #         do_task(task_data['service_path'], task_data['method'], task_data['params'])
    # except Exception, e:
    #     print Exception, ':', e

    # time.sleep(0)
    # run(params)


if __name__ == '__main__':
    argv_list = []
    for i in range(pool_size):
        argv_list.append({})
    requests = threadpool.makeRequests(run, argv_list)
    [pool.putRequest(req) for req in requests]
    pool.wait()
