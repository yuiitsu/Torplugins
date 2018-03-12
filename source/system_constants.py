# -*- coding:utf-8 -*-

"""
@author: delu
@file: system_constants.py
@time: 17/4/28 下午5:21
"""


class SystemConstants(object):

    SUCCESS = {'code': 0, 'msg': '成功'}
    REMOTE_SERVICE_ERROR = {'code': 1107, 'msg': '调用远程服务请求失败'}
    SCHEDULE_ADD_JOB_ERROR = {'code': 1108, 'msg': '添加schedule job失败'}
    SCHEDULE_REMOVE_JOB_ERROR = {'code': 1109, 'msg': '移除schedule job 失败'}
