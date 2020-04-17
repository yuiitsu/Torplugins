# -*- coding: utf-8 -*-

"""
@author: Yuiitsu
@file: monitor
@time: 2018/6/13 11:26
"""
import asyncio

from tools.logs import Logs
from tools.date_utils import DateUtils
from source.properties import Properties
# from source.redisbase import RedisBase
from source.async_redis import AsyncRedis
from .report import Report
import task

properties = Properties('task')
logger = Logs().logger
date_utils = DateUtils()
# redis = RedisBase()
redis = AsyncRedis()


class Monitor(object):
    task_queue_length = 0
    task_queue_report_num = 0
    task_queue = properties.get('cache', 'task_queue')
    failed_queue = properties.get('cache', 'failed_queue')

    @classmethod
    async def start(cls):
        """
        监控loop
        :return:
        """
        logger.info("Monitor start.")
        while True:
            # 检查失败队列
            try:
                failed_queue_len = await redis.llen(cls.failed_queue)
            except Exception as e:
                await Report.report("获取failed queue len失败", e.args[0])
                continue

            if failed_queue_len > 0:
                try:
                    failed_task = await redis.lrange(cls.failed_queue, 0, 10)
                except Exception as e:
                    await Report.report("获取失败任务数据失败", e.args[0])
                    continue

                failed_task_html = ['<tr><td style="font-size:30px;">有失败任务，请检查.</td></tr>']
                for item in failed_task:
                    failed_task_html.append('<tr><td>{}</td></tr>'.format(item))

                await Report.report("", cls.mail_template("".join(failed_task_html)))
            else:
                pass
                # logger.info('失败任务检查正常.')

            # 检查任务队列
            try:
                await cls.check_queue()
            except Exception as e:
                await Report.report("获取failed queue len失败", e.args[0])
                continue

            await asyncio.sleep(10)

    @classmethod
    async def check_queue(cls):
        """
        检查任务队列
            每10秒检查一次，如果任务队列的长度比前一次检查的长度长，且前一次检查长度不为0，那么发送报警邮件
        :return:
        """
        try:
            task_queue_len = await redis.llen(cls.task_queue)
        except Exception:
            raise

        if task_queue_len > 0:
            if (cls.task_queue_length > 0) and (task_queue_len >= cls.task_queue_length):
                if cls.task_queue_report_num >= 3:
                    report_html = """
                        <tr>
                            <td style="font-size:30px;">任务队列未能即时消费，当前任务数量：{}，前一次检查任务数量：{}，请注意.</td>
                        </tr>
                        <tr>
                            <td>可能原因：</td>
                        </tr>
                        <tr>
                            <td>1.任务消费能力不足。 如果是，程序将在3次检查之后自动增加消费者进行处理。之后如果仍然不能停止报警，见2</td>
                        </tr>
                        <tr>
                            <td>2.任务进程死亡。检查任务死亡原因，并重启服务</td>
                        </tr>
                        <tr>
                            <td>Task Monitor report at: {}</td>
                        </tr>
                    """.format(task_queue_len, cls.task_queue_length, DateUtils.time_now())
                    await Report.report("", cls.mail_template(report_html))

                    if cls.task_queue_report_num >= 6:
                        await task.add("", "", None, False, {
                            'loop_num': 1,
                        })
                else:
                    cls.task_queue_report_num = cls.task_queue_report_num + 1
            else:
                cls.task_queue_report_num = 0

            cls.task_queue_length = task_queue_len

    @classmethod
    def mail_template(cls, content):
        """
        邮件模板
        :param content:
        :return:
        """
        return '' \
               '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">' \
               '<html xmlns="http://www.w3.org/1999/xhtml">' \
               '<head>' \
               '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />' \
               '<title>Task Error</title>' \
               '<meta name="viewport" content="width=device-width, initial-scale=1.0"/>' \
               '</head>' \
               '<body>' \
               '<table  border="0" cellpadding="10" cellspacing="0" width="100%">{}</table>' \
               '</body>' \
               '</html>'.format(content)
