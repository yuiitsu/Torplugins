#!usr/bin/env python
# -*- coding:utf-8 -*-

import hashlib
import json
import random
import re
import time

import tornado.gen

from constants.error_code import Code
from source.controller import Controller
from source.properties import Properties
from source.async_redis import AsyncRedis
from source.service_manager import ServiceManager as serviceManager
from tools.date_json_encoder import CJsonEncoder
from tools.logs import Logs
from tools.common_util import CommonUtil


class Base(Controller):

    json = json
    time = time
    redis = AsyncRedis()
    error_code = Code
    properties = Properties()
    logger = Logs().logger
    _params = {}

    @tornado.gen.coroutine
    def prepare(self):
        """
        接受请求前置方法
            1.解析域名
            2.检查IP限制
            3.权限检查
        :return:
        """
        self._params = self.get_params()

    def out(self, data):
        """ 
        输出结果
        :param data: 返回数据字典
        """
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(self.json.dumps(data, cls=CJsonEncoder))

    def error_out(self, error, data=''):
        """
        错误输出
        :param error: 错误信息对象
        :param data: 返回数据字典
        :return: 
        """
        out = error
        if data:
            out['data'] = data

        self.write(out)

    @tornado.gen.coroutine
    def get(self):
        """
        重写父类get方法，接受GET请求
        如果执行到此方法，说明请求类型错误
        """
        self.error_out(self._e('REQUEST_TYPE_ERROR'))

    @tornado.gen.coroutine
    def post(self):
        """
        重写父类post方法，接受POST请求
        如果执行到此方法，说明请求类型错误
        """
        self.error_out(self._e('REQUEST_TYPE_ERROR'))

    def do_service(self, service_path, method, params):
        """
        调用服务
        :param service_path: 
        :param method: 
        :param params: 
        :return: 
        """
        version = CommonUtil.get_loader_version(service_path)
        power_tree = self.settings['power_tree']
        return serviceManager.do_service(service_path, method, params=params, version=version,
                                         power=power_tree)

    def _e(self, error_key):
        """
        :param error_key:
        :return: 
        """
        data = {}
        for key in self.error_code[error_key]:
            data[key] = self.error_code[error_key][key]

        return data

    def _gr(self, data):
        """
        tornado.gen.Return
        :param data: 数据
        :return:
        """
        return tornado.gen.Return(data)

    def params(self, key=''):
        """
        获取参数中指定key的数据
        :param key:
        :return:
        """
        if not key:
            return self._params
        elif key not in self._params:
            return ''
        else:
            return self._params[key]

    def get_user_agent(self):
        """
        获取用户访问数据
        :return:
        """
        request = self.request
        if 'Remote_ip' in request.headers and request.headers['Remote_ip']:
            ip = request.headers['Remote_ip']
        elif 'X-Forward-For' in request.headers and request.headers['X-Forward-For']:
            ip = request.headers['X-Forward-For']
        else:
            ip = request.remote_ip

        cookies = ''
        if request.cookies:
            for k, v in request.cookies.items():
                cookies += k + '=' + v.value + ';'

        try:
            user_agent = request.headers['User-Agent']
        except Exception as e:
            user_agent = ''

        return {
            'remote_ip': ip,
            'user_agent': user_agent,
            'cookies': cookies
        }
