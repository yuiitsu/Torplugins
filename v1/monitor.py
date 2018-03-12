# -*- coding:utf-8 -*-

"""
@author onlyfu
@time 11/2/2017
"""
import sys
sys.path.append("../")
import time
import smtplib
import json
from email.mime.text import MIMEText

from constants.cachekey_predix import CacheKeyPredix
from source.redisbase import RedisBase
from source.properties import properties
from tools.date_utils import DateUtils
from tools.logs import Logs

redis = RedisBase()
list_cache_key = CacheKeyPredix.TASK_DATA_LIST
logger = Logs().logger

try:
    warning_to_email = properties.get('monitor', 'MAIL_LIST')
    warning_to_email = warning_to_email.split(',')
except Exception, e:
    warning_to_email = None
    print e

# warning_to_email = [
#     'macys-alert@wemart.cn',
#     'onlyfu@wemart.cn'
# ]


def send_warning_info(warning_type, msg):
    """
    发送报警信息
    :param warning_type: 警告类型, monitor: 监控警告， task: 队列任务警告
    :param msg: 消息内容
    :return:
    """
    send_success_num = 0
    for email in warning_to_email:
        try:
            pre_subject = '[{} error]'.format(warning_type)
            content = '{} {}'.format(pre_subject, msg)
            send_pwd = properties.get('messages', 'EMAIL_AUTHKEY')
            send_address = properties.get('messages', 'SEND_ADDRESS')
            mail_host = 'smtp.exmail.qq.com'
            mime_content = MIMEText(content, _subtype='plain', _charset='UTF-8')
            mime_content['From'] = send_address
            mime_content['To'] = email
            mime_content['Subject'] = pre_subject
            me = '<' + send_address + '>'
            server = smtplib.SMTP_SSL()
            server.connect(mail_host, 465)
            server.login(send_address, send_pwd)
            server.sendmail(me, [email], mime_content.as_string())
            server.quit()
            send_success_num += 1
            logger.info('send warning mail success, to: %s, subject: %s, content: %s', email, pre_subject, content)
        except Exception, e:
            logger.error('send warning mail failed, e: %s', e.message)

    if send_success_num > 0:
        return True
    else:
        return False


def run():
    """
    开始执行
    :return:
    """
    if warning_to_email is None:
        print 'warning mail error, check setting.conf [monitor]'
        return

    last_len = 0
    loop_num = 0
    conn_failed_num = 0
    while True:
        try:
            conn = redis.get_conn()
            list_len = conn.llen(list_cache_key)
        except Exception, e:
            conn_failed_num += 1
            if conn_failed_num >= 6:
                response = send_warning_info('monitor', json.dumps({
                    'exception message': e.message,
                    'time': DateUtils.time_now()
                }))
                if response is True:
                    conn_failed_num = 0

            list_len = 0
            logger.error('monitor redis get_conn failed, e: %s', e.message)

        if list_len > 0 and list_len >= last_len:
            loop_num += 1
            # 队列长度保持不变或增加
            if loop_num >= 6:
                response = send_warning_info('task', json.dumps({
                    'list_len': list_len,
                    'time': DateUtils.time_now()
                }))
                if response is True:
                    loop_num = 0
            else:
                logger.info('task len add')
        else:
            last_len = list_len
            loop_num = 0
            # print 'task status is normal'

        time.sleep(10)


if __name__ == '__main__':
    run()
    # send_warning_info('task', json.dumps({
    #     'list_len': '1024',
    #     'time': DateUtils.time_now()
    # }))
