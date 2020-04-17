# -*- coding:utf-8 -*-

"""
@author: delu
@file: schedule_manager.py
@time: 18/6/20 14:08
定时任务运行流程
web端:
    将任务添加至队列，根据任务执行时间，向最近的30s向后靠近，例如，任务执行时间为2018年6月20日 17时18分42秒，
    那么最终执行时间为2018年6月20日 17时19分0秒
    那么此时对应缓存的key为job_20180620171900(这是一个list)

schedule端:
    一、启动时读取数据库端任务，根据任务的下一次执行时间依次生成对应的key，如果任务已过期，则立即执行，并且计算下一次需要执行的时间。
    如果是单次任务，则直接从数据库删除该条任务的记录
    二、主线程每隔1秒遍历需要执行的key，假如当前时间为2018年6月20日 14时21分07秒，则主线程需要检查当前时间是否为第0秒或者第30秒。如果
    刚好是第0秒或者第30秒，则获取这个时间点对应的job队列(例如，当前是2018-06-20 17:18:00，则获取job_20180620171800对应的所有元素,
    job_20180620171800是redis里set数据结构对应的key)，如果不是，则暂停1秒后，继续检查。
"""
import os
import sys


parent_path = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.dirname(parent_path)
sys.path.append(parent_path)
sys.path.append(root_path)


import asyncio
import datetime
import time
import json
import importlib

from base.service import ServiceBase
from source.async_model import AsyncModelBase
from source.async_redis import AsyncRedis
from tools.date_json_encoder import CJsonEncoder
from tools.date_utils import DateUtils
from tools.logs import Logs
from tools.cron_utils import CronUtils
from source.properties import Properties
from task.schedule.path_conf import CONF
import task

# redis = RedisBase()
redis = AsyncRedis()
logger = Logs().logger
cron_utils = CronUtils()
properties = Properties('schedule')

intervals = int(properties.get('schedule', 'intervals'))
run_time = int(properties.get('schedule', 'run_time'))
SCHEDULE_KEY = properties.get('schedule', 'schedule_key')
JOB_KEY = properties.get('schedule', 'job_key')
key_YYMMDDHHMM = '%Y%m%d%H%M'
key_YYMMDDHHMMSS = '%Y%m%d%H%M%S'


async def do_job_list(job_list, is_normal=True):
    """
    开协程执行定时任务
    job_list 需要执行的任务列表
    is_normal 是否正常执行任务  True正常任务 ,  False 过期任务补偿执行
    :return: 
    """
    for job in job_list:
        try:
            if isinstance(job, str):
                job = json.loads(job)
            await do_job(job, is_normal)
        except Exception as e:
            logger.exception('JSON ERROR', e)
            await task.save_task_error(job, e)


async def do_job(job, is_normal=True):
    """
    执行定时任务
    :param job: 
    job {
        job_id: xxx,             任务编号
        group_name: xxx,         任务分组名
        start_time: xxx,         开始时间
        limit_time: xxx,         剩余时间
        repeat_count: xxx,       重复次数(-1为无限循环)
        cron: xxx,               cron表达式
        path: xxxx,              service路径
        method: xxxx,            方法名
        params: xxxxx,           参数
    }
    :param is_normal
    :return: 
    """
    try:
        logger.info('执行任务: %s----%s\n\n', job['job_id'], job)
        result = None
        try:
            result = await ServiceBase().do_service(job['path'], job['method'], job['params'])
        except Exception as e:
            pass
        if int(job['repeat_count']) == -1:
            # 不管本次任务执行成功或者失败，都会计算下一次任务的执行时间
            await cal_next_start_time(job, is_normal)
        # 1. 如果错误码不为0，则判断对应的path的method是否应该被忽略
        if (result['code'] != 0 and result['code'] not in CONF) or \
                (result['code'] in CONF and job['path'] not in CONF[result['code']]) or \
                (result['code'] in CONF and job['path'] in CONF[result['code']] and
                         job['method'] not in CONF[result['code']][job['path']]):
            raise ValueError(result)

        if int(job['repeat_count']) != -1:
            # 任务成功执行，删除对应的数据库记录
            await remove_job(job)

    except Exception as e:
        await task.save_task_error(job, e)
        logger.exception(e)


async def cal_next_start_time(job, is_normal=True):
    """
    计算下一次定时任务发生的时间
    :param job: 
    :param is_normal
    :return: 
    """
    # 无限循环执行, 必定带正则表达式，否则直接报错
    # 解析正则表达式,  计算出下一次需要执行的时间点
    if not is_normal:
        current_time = int(DateUtils.timestamps_now())
    else:
        current_time = DateUtils.str_to_time(job['start_time'])
    left_time = cron_utils.analyze(current_time + 1, job['cron'])
    start_time = DateUtils.format_time(current_time + left_time)
    # 计算距离start_time最近的RUN_TIME秒
    current_date = start_time[:16] + ':00'
    current_count = 1
    while current_date < start_time:
        # 避免死循环
        if current_count >= 1000:
            break
        current_count += 1
        current_date = DateUtils.add_second(current_date, seconds=run_time)
    start_time = current_date
    job['start_time'] = start_time
    cache_key = ServiceBase.schedule.JOB_KEY + job['start_time'].replace(' ', '').replace('-', '').replace(':', '')
    now_date = DateUtils.time_now()
    # 如果下一次的执行时间小于当前时间，则跳至下一个执行的时间节点
    if job['start_time'] < now_date:
        logger.info('任务下一次执行时间小于当前时间')

        current_date = now_date[:16] + ':00'

        while current_date < now_date:

            current_date = DateUtils.add_second(current_date, seconds=2 * run_time)

        job['start_time'] = current_date

        cache_key = ServiceBase.schedule.JOB_KEY + job['start_time'].replace(' ', '').replace('-', '').replace(':', '')

    model = importlib.import_module('task.schedule.model')
    model = model.Model()
    await model.update_job(job)
    await redis.sadd(cache_key, json.dumps(job, cls=CJsonEncoder))
    length = await redis.scard(cache_key)
    await redis.hset(ServiceBase.schedule.SCHEDULE_KEY, cache_key, length)


async def remove_job(job):
    """
    从数据库移除任务
    :param job: 
    :return: 
    """
    model = importlib.import_module('task.schedule.model')
    model = model.Model()
    result = await model.delete_job(job)
    if not result:
        await task.save_task_error(job, ValueError(result))


async def get_job_list():
    """
    从数据库获取任务
    :return: 
    """
    logger.info('从数据库获取任务')
    model = AsyncModelBase()
    condition = ' path != %s and method != %s '
    value_tuple = ('', '')
    job_list = await model.find('tbl_cfg_schedule_job',
                                {
                                    model.sql_constants.CONDITION: condition
                                },
                                value_tuple,
                                model.sql_constants.LIST)
    return job_list


async def add_job(job_list):
    """
    添加任务至任务队列
    :param job_list: 
    :return: 
    """
    logger.info('添加任务至队列')
    current_time = DateUtils.time_now()
    if job_list:
        for job in job_list:
            if isinstance(job['params'], str):
                try:
                    job['params'] = json.loads(job['params'])
                except Exception as e:
                    logger.exception('JSON ERROR', e)
            del job['create_time']
            try:
                cache_key = ServiceBase.schedule.JOB_KEY + job['start_time'].replace(' ', '').replace('-', '').replace(
                    ':', '')
                if current_time >= job['start_time']:
                    # 当前时间大于任务执行时间, 则立刻执行任务, 然后删除当前的key
                    await do_job(job, is_normal=False)
                    await redis.delete(cache_key)
                else:
                    # 将任务添加进对应的队列组, 采用set所以当添加重复元素时，重复元素会被忽略
                    await redis.sadd(cache_key, json.dumps(job, cls=CJsonEncoder))
                    length = await redis.scard(cache_key)
                    await redis.hset(ServiceBase.schedule.SCHEDULE_KEY, cache_key, length)
            except Exception as e:
                logger.exception('ADD JOB ERROR', e)
                await task.save_task_error(job, e)


def start():
    """
    从数据读取数据并执行
    :return: 
    """
    event_loop = asyncio.get_event_loop()
    asyncio.ensure_future(delete_cache_key())
    asyncio.ensure_future(run())
    event_loop.run_forever()


async def delete_cache_key():
    """
    删除redis中所有遗留的key
    :return:
    """
    logger.info('删除遗留的cache key')
    job_key_dict = await redis.hgetall(ServiceBase.schedule.SCHEDULE_KEY)
    for key in job_key_dict.keys():
        await redis.delete(key)
    await redis.delete(ServiceBase.schedule.SCHEDULE_KEY)


async def run():
    """
    每隔1秒读取任务
    :return: 
    """
    job_list = await get_job_list()
    await add_job(job_list)
    while True:
        await do_schedule()
        await asyncio.sleep(intervals)


async def do_schedule():
    """
    扫描下一个时间点可以执行的定时任务
    :return: 
    """
    current_datetime = datetime.datetime.now()
    current_second = current_datetime.second

    quotient = int(current_second / run_time)
    remainder = int(current_second % run_time)
    if remainder > 0:
        quotient = quotient + 1
    next_second = quotient * run_time
    if next_second == 60:
        next_datetime = current_datetime + datetime.timedelta(minutes=1)
        next_second = 0
    else:
        next_datetime = current_datetime
    next_timestamp = time.mktime(next_datetime.timetuple())
    next_time = DateUtils.format_time(next_timestamp, time_format=key_YYMMDDHHMM)
    # 当前时间点位于0秒或者30秒，则读取job队列并执行
    cache_key = ServiceBase.schedule.JOB_KEY + next_time + format_second(next_second)
    job_list = await redis.smembers(cache_key)
    if job_list:
        # 开协程执行任务
        await do_job_list(job_list)
    await redis.delete(cache_key)
    await redis.hdel(ServiceBase.schedule.SCHEDULE_KEY, cache_key)


def format_second(second):
    if second < 10:
        return '0' + str(second)
    else:
        return str(second)


if __name__ == '__main__':
    # add_job_test()
    logger.info('schedule 启动啦!!')
    start()
