# -*- coding:utf-8 -*-

import datetime
import hashlib
import importlib
import json
import time
from functools import wraps

import tornado.escape
import tornado.gen

import task
from task import schedule
from constants.error_code import Code
from source.properties import Properties
from source.async_redis import AsyncRedis
from source.service_manager import ServiceManager as serviceManager
from tools.common_util import CommonUtil
from tools.httputils import HttpUtils
from tools.logs import Logs
from language.manager import LangManager


class ServiceBase(object):
    time = time
    datetime = datetime
    json = json
    hashlib = hashlib
    error_code = Code
    properties = Properties()
    redis = AsyncRedis()
    http_utils = HttpUtils
    common_utils = CommonUtil
    logger = Logs().logger
    lang = LangManager()
    task = task
    schedule = schedule

    def import_model(self, model_name):
        """
        加载数据类
        :param model_name: string 数据类名
        :return:
        """
        try:
            version = self.common_utils.get_loader_version()
            model = importlib.import_module('src.module.' + version + '.' + model_name)
            return model.Model()
        except Exception as e:
            self.logger.exception(e)
            return None

    def do_service(self, service_path, method, params):
        """
        调用服务
        :param service_path: 
        :param method: 
        :param params: 
        :return: 
        """
        version = self.common_utils.get_loader_version(service_path)
        return serviceManager.do_service(service_path, method, params=params, version=version)

    @tornado.gen.coroutine
    def load_extensions(self, trigger_position, data):
        """
        加载扩展程序
        :param trigger_position:
        :param data:
        :return:
        """
        data['trigger_position'] = trigger_position
        result = yield self.do_service('v1.cfg.extensions.service', 'query', {'trigger_position': trigger_position})
        if result and 'code' in result and result['code'] == 0:
            # 发送消息
            for item in result['data']:
                service_path = item['package_path']
                method = item['method']
                yield self.task.add(service_path, method, data)

    def _e(self, error_key):
        """
        :param error_key: 
        :return: 
        """
        data = {}
        for key in self.error_code[error_key]:
            data[key] = self.error_code[error_key][key]

        return data

    def _gre(self, data):
        """
        tornado.gen.Return
        :rtype:
        :param data: 数据
        :return: 
        """
        return tornado.gen.Return(self._e(data))

    def _gree(self, error_key, customer_msg):
        """
        自定义扩展错误信息
        :param error_key: 
        :param customer_msg: 自定义额外错误信息
        :return: 
        """
        result = self._e(error_key)
        if customer_msg:
            result['msg'] += '({})'.format(customer_msg)
        return tornado.gen.Return(result)

    def _grs(self, data):
        """
        成功返回
        :param data: 
        :return: 
        """
        result = self._e('SUCCESS')
        result['data'] = data
        return tornado.gen.Return(result)

    def _gr(self, data):
        """
        tornado.gen.Return
        :param data: 数据
        :return: 
        """
        return tornado.gen.Return(data)

    @classmethod
    def params_set(cls, model=None, data=None):
        """
        数据对象设置
        :param model:
        :param data:
        :return:
        """
        def decorate(func):
            @wraps(func)
            @tornado.gen.coroutine
            def wrapper(*args, **kwargs):
                o = args[0]
                params = args[1]
                model_data = None
                if hasattr(o, model):
                    model_obj = getattr(o, model)
                    if hasattr(model_obj, data):
                        model_data = getattr(model_obj, data)

                new_args = args
                if model_data:
                    if isinstance(params, dict):
                        model_data.update(params)
                        new_args = (args[0], model_data)

                result = yield func(*new_args, **kwargs)

                return result

            return wrapper
        return decorate
