# -*- coding:utf-8 -*-

"""
@author: delu
@file: __init__.py.py
@time: 18/6/20 14:07
"""
import importlib

from source.properties import Properties
from tools.cron_utils import CronUtils
from tools.date_utils import DateUtils
from constants.error_code import Code

cron_utils = CronUtils()
properties = Properties('schedule')
SCHEDULE_KEY = properties.get('schedule', 'schedule_key')
JOB_KEY = properties.get('schedule', 'job_key')
RUN_TIME = int(properties.get('schedule', 'run_time'))


async def async_add_job(service_path='', method='', params={}, start_time='', cron='', job_id='', group_name='default',
                        repeat_count=0):
    """
    添加定时任务
    :param service_path:   需要执行的service路径
    :param method:         需要执行的方法
    :param params:         需要传入的参数
    :param start_time: (2018-06-20 16:30:00)
    :param cron: 这里采用五位表达式，从左到右依次表示秒、分、时、天、月  
                 可以使用具体数字或者区间
                 20  表示[20]
                 1-3 表示[1, 2, 3]  
                 1,4,6,7 表示[1, 4, 6, 7]
                 * 表示所有, 
                 1/5 从第1个开始，每五个执行一次
    :param job_id:       任务编号，每个任务的编号都要求唯一
    :param group_name: 
    :param repeat_count: 如果要求无限次执行, 则该值需要传入-1, 同一个任务有限次多次执行的情况暂不考虑,
                         如果业务上有需要, 希望你用多个任务来处理这件事
    :return: 
    """
    if cron:
        current_time = int(DateUtils.timestamps_now())
        left_time = cron_utils.analyze(current_time + 1, cron)
        start_time = DateUtils.format_time(current_time + left_time)
    # 计算距离start_time最近的RUN_TIME秒
    current_date = start_time[:16] + ':00'
    current_count = 1
    while current_date < start_time:
        # 避免死循环
        if current_count >= 1000:
            break
        current_count += 1
        current_date = DateUtils.add_second(current_date, seconds=RUN_TIME)
    start_time = current_date

    job_params = {
        'job_id': job_id,
        'group_name': group_name,
        'start_time': start_time,
        'limit_time': 0,
        'repeat_count': repeat_count,
        'cron': cron,
        'path': service_path,
        'method': method,
        'params': params
    }
    result = await save_job(job_params)
    return result


async def save_job(job_params):
    """
    保存任务至数据库
    :param job_params: 
    :return: 
    """
    model = importlib.import_module('task.schedule.model')
    model = model.Model()
    result = await model.save_job(job_params)
    if result:
        cache_job_key = JOB_KEY + job_params['start_time'].replace(' ', '').replace('-', '').replace(':', '')
        await model.redis.sadd(cache_job_key, model.json.dumps(job_params, cls=model.date_encoder))
        set_length = await model.redis.scard(cache_job_key)
        await model.redis.hset(SCHEDULE_KEY, cache_job_key, str(set_length))
    return result

async def update_job(job_id='', start_time=''):
    """
    更新定时任务时间
    :param job_id: 
    :param start_time: 
    :return: 
    """
    model = importlib.import_module('task.schedule.model')
    model = model.Model()
    job_result = await query_job_one(job_id)
    if not job_result:
        return Code['CFG_SCHEDULE_JOB_NOT_FOUND']
    if isinstance(job_result['params'], str):
        try:
            job_result['params'] = model.json.loads(job_result['params'])
        except Exception as e:
            model.logger.exception('JSON ERROR', e)
    del job_result['create_time']
    job_result['start_time'] = start_time
    result = await model.update_job(job_result)
    if not result:
        return Code['SQL_EXECUTE_ERROR']
    cache_job_key = JOB_KEY + job_result['start_time'].replace(' ', '').replace('-', '').replace(':', '')
    await model.redis.sadd(cache_job_key, model.json.dumps(job_result, cls=model.date_encoder))
    set_length = await model.redis.scard(cache_job_key)
    await model.redis.hset(SCHEDULE_KEY, cache_job_key, str(set_length))
    return result


async def remove_job(job_id=''):
    """
    从数据库移除任务
    :param job_id: 
    :return: 
    """
    model = importlib.import_module('task.schedule.model')
    model = model.Model()
    job_result = await model.query_job_one({
        'job_id': job_id
    })
    if not job_result:
        return Code['SQL_EXECUTE_ERROR']
    try:
        if isinstance(job_result['data']['params'], str):
            job_result['data']['params'] = model.json.loads(job_result['data']['params'])
    except Exception as e:
        model.logger.exception('JSON ERROR', e)
        return Code['JSON_DATA_FORMAT_ERROR']
    start_time = job_result['data']['start_time']
    cache_key = JOB_KEY + start_time.replace(' ', '').replace('-', '').replace(':', '')
    del job_result['data']['create_time']
    result = await model.delete_job({
        'job_id': job_id
    })
    if not result:
        return Code['SQL_EXECUTE_ERROR']
    await model.redis.srem(cache_key, model.json.dumps(job_result['data'], cls=model.date_encoder))

async def query_job_one(job_id):
    """
    查询任务记录
    :param job_id: 
    :return: 
    """
    model = importlib.import_module('task.schedule.model')
    model = model.Model()
    result = await model.query_job_one({
        'job_id': job_id
    })
    return result
