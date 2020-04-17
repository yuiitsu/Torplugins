# -*- coding: utf-8 -*-

"""
@author: Yuiitsu
@file: runner
@time: 2018/6/5 11:36
"""
import os
import sys
import random


parent_path = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.dirname(parent_path)
sys.path.append(parent_path)
sys.path.append(root_path)


import asyncio
import json
import configparser

import task
from base.service import ServiceBase
from tools.logs import Logs
from tools.common_util import CommonUtil
from tools.date_utils import DateUtils
from task.monitor import Monitor
from task.report import Report

logger = Logs().logger


class TaskRunner(object):

    server_name = ''
    is_running = True

    def run(self):
        # 获取参数
        loop_num = 0
        config_file = ''
        arguments = sys.argv
        for k, v in enumerate(arguments):
            if v == '-t':
                loop_num = arguments[k + 1]

            if v == '-c':
                config_file = arguments[k + 1]

            if v == '-s':
                self.server_name = arguments[k + 1]

        if config_file:
            self.parse_config(config_file)

        if loop_num:
            task.loop_num = loop_num

        #
        if not self.server_name:
            self.server_name = 'S' + str(random.randrange(10000, 100000))

        event_loop = asyncio.get_event_loop()
        # register server
        asyncio.ensure_future(task.register_server(server_name=self.server_name, create_time=int(DateUtils.timestamps_now())))

        # main loop
        for i in range(task.loop_num):
            asyncio.ensure_future(self.loop(str(i)))

        # monitor loop
        # asyncio.ensure_future(Monitor.start())

        event_loop.run_forever()

    async def loop(self, task_id):
        """
        1. 获取一个队列数据
        2. 解析数据
        3. 调用目标方法
        :return:
        """
        logger.info('task[%s] started.', task_id)
        await task.register_coroutine(self.server_name, task_id, int(DateUtils.timestamps_now()))
        await self.process(task_id)

    def create_sub_task(self, task_data):
        """
        创建子任务
        :param task_data:
        :return:
        """
        loop_num = task_data.get('loop_num', 0)
        task_queue_key = task_data.get('task_queue_key', None)
        sub_task_id = CommonUtil.create_uuid()

        if loop_num > 0:
            for i in range(loop_num):
                asyncio.ensure_future(self.sub_task(sub_task_id + '_' + str(i), task_queue_key=task_queue_key))

    async def sub_task(self, task_id, task_queue_key=None):
        """
        子任务
        :param task_id:
        :param task_queue_key:
        :return:
        """
        logger.info('sub task[%s] started.', task_id)
        await self.process(task_id, task_queue_key, is_break=True)

    # async def check_server_status(self):
    #     """
    #     检查服务开关状态
    #     :return:
    #     """
    #     while True:
    #         status = await task.get_server_status(self.server_name)
    #         if not status or status == '0':
    #             self.is_running = False
    #
    #         await asyncio.sleep(10)

    async def process(self, task_id, task_queue_key=None, is_break=False):
        """
        处理任务
        :param task_id: 任务ID
        :param task_queue_key: 指定队列的缓存KEY
        :param is_break: 是否需要停止循环
        :return:
        """
        while True:
            #
            status = await task.get_server_status(self.server_name)
            if not status or status == '0':
                logger.info('Server [%s] shutdown, task [%s] shutdown', self.server_name, task_id)
                self.is_running = False
                await asyncio.sleep(10)
                continue

            if not self.is_running:
                self.is_running = True
                logger.info('Server [%s] start, task [%s] start', self.server_name, task_id)
            #
            is_process_success = 'success'
            task_unique_id = ''
            item = await task.get_one(task_queue_key)
            if item is False:
                logger.info('Server [%s], task [%s], get seed failed.', self.server_name, task_id)
                await Report.report('获取任务异常', '')

            if item:
                try:
                    target = json.loads(item)
                    task_unique_id = target.get('task_unique_id', '')
                    path = target['path']
                    method = target['method']
                    params = target['arguments']
                    sub_task = target['sub_task']
                    #
                    logger.info('Task [%s] Pop [%s] from queue, path [%s], method [%s], params: %s',
                                task_id, task_unique_id, path, method, json.dumps(params))
                    #
                    if sub_task:
                        self.create_sub_task(sub_task)
                    else:
                        result = await ServiceBase().do_service(path, method, params)
                        logger.info('task[%s], path: %s, method: %s result: %s', task_id, path, method, result)
                        if not result or 'code' not in result or (result['code'] != 0 and result['code'] != 1004):
                            # failed
                            raise ValueError(result)
                except Exception as e:
                    logger.exception(e)
                    is_process_success = 'failed'
                    await task.save_task_error(item, e)
                #
                if task_unique_id:
                    await task.update_to_db(task_unique_id, is_process_success)
            else:
                # logger.info('task[%s] wait seed.', task_id)
                if is_break:
                    logger.info('task[%s] break.', task_id)
                    break

            #
            await task.refresh_coroutine(self.server_name, task_id, int(DateUtils.timestamps_now()))
            await asyncio.sleep(1)

    def parse_config(self, config_path):
        """
        解析配置文件
        :param config_path:
        :return:
        """
        if config_path:
            handler = configparser.ConfigParser()
            try:
                handler.read(config_path)
                task.loop_num = handler.get('loop', 'loop_num')
            except Exception as e:
                logger.exception(e)


if __name__ == '__main__':
    TaskRunner().run()
