# -*- coding:utf-8 -*-

"""
@author: delu
@file: httputils.py
@time: 17/5/2 上午10:36
"""
import urllib
import urllib2
import json
import tornado.gen
from tornado.httpclient import HTTPRequest
from tornado.httpclient import AsyncHTTPClient
from tornado.httpclient import HTTPClient
from source.model import ModelBase
import inspect
from tools.logs import Logs

logger = Logs().logger


class HttpUtils(object):
    @staticmethod
    def do_get(url, params=''):
        """
        发送get请求
        :param url: 
        :param params: 
        :return: 
        """
        print '发送请求 url: %s, params : ' % url
        print params
        url_params = '?'
        if len(params) > 0:
            for key in params:
                url_params += '%s=%s&' % (key, params[key])
            url += url_params + 'x=1'
        req = urllib2.Request(url)
        res_data = urllib2.urlopen(req)
        res = res_data.read()
        print '请求结果 %s' % res
        return res

    @staticmethod
    def do_post(url, params={}, headers={}):
        """
        发送post请求
        :param url: 
        :param params: 
        :return: 
        """
        print '发送请求 url: %s, params: ' % url
        print params
        params_urlencode = params if isinstance(params, str) else urllib.urlencode(params)
        if headers:
            req = urllib2.Request(url=url, data=json.dumps(params, ensure_ascii=False), headers=headers)
        else:
            req = urllib2.Request(url=url, data=params_urlencode)
        res_data = urllib2.urlopen(req)
        res = res_data.read()
        print '请求结果 %s' % res
        return res

    @staticmethod
    def do_post_with_cert(url, params={}, headers={}, client_key=None, client_cert=None):
        body = params if isinstance(params, str) else urllib.urlencode(params)
        http_request = HTTPRequest(url, 'POST', body=body, headers=headers, validate_cert=False, client_key=client_key,
                                   client_cert=client_cert)
        http_client = HTTPClient()
        fetch_result = http_client.fetch(http_request)
        return fetch_result.body

    @staticmethod
    @tornado.gen.coroutine
    def get(url, params={}):
        url_params = '?'
        if len(params) > 0:
            for key in params:
                url_params += '%s=%s&' % (key, params[key])
            url += url_params + 'x=1'

        http_request = HTTPRequest(url, 'GET', validate_cert=False)
        http_client = AsyncHTTPClient()
        return_data = None
        try:
            fetch_result = yield http_client.fetch(http_request)
            return_data = fetch_result.body
        except Exception, e:
            print e

        raise tornado.gen.Return(return_data)

    @staticmethod
    @tornado.gen.coroutine
    def post(url, params={}, headers={}):
        body = params if isinstance(params, str) else urllib.urlencode(params)
        http_request = HTTPRequest(url, 'POST', body=body, headers=headers, validate_cert=False)
        http_client = AsyncHTTPClient()
        return_data = None
        try:
            fetch_result = yield http_client.fetch(http_request)
            return_data = fetch_result.body
        except Exception as e:
            logger.exception(e)

        raise tornado.gen.Return(return_data)

    @staticmethod
    @tornado.gen.coroutine
    def post_with_cert(url, params={}, headers={}, client_key=None, client_cert=None):
        body = params if isinstance(params, str) else urllib.urlencode(params)
        http_request = HTTPRequest(url, 'POST', body=body, headers=headers, validate_cert=False, client_key=client_key,
                                   client_cert=client_cert)
        http_client = AsyncHTTPClient()
        fetch_result = yield http_client.fetch(http_request)
        raise tornado.gen.Return(fetch_result.body)

    @staticmethod
    def write_log(params):
        """
        写入日志
        :param params:
        :return:
        """
        try:
            log_id = params.get('log_id', '')
            model = ModelBase()
            logger = Logs().logger
            path = ''
            method = ''
            stack_back = inspect.currentframe()
            for i in range(len(inspect.stack())):
                stack_back = stack_back.f_back

                if stack_back and stack_back.f_locals.get('service_path', ''):
                    path = stack_back.f_locals.get('service_path', '')
                    method = stack_back.f_locals.get('method', '')
                    break
            if not log_id:
                insert_params = {
                    'transfer_method': params['transfer_method'],
                    'addr': params['addr'],
                    'path': path,
                    'method': method,
                    'params': params['params'],
                    'result': '',
                }
                # 没有log_id则插入
                key = 'transfer_method, addr, path, method, params, result'
                val = '%s, %s, %s, %s, %s, %s'
                value_tuple = (insert_params['transfer_method'], insert_params['addr'], insert_params['path'],
                               insert_params['method'], insert_params['params'], insert_params['result'])

                result = model.insert('tbl_thirdpart_connection_logs', {
                    model.sql_constants.KEY: key,
                    model.sql_constants.VAL: val
                }, tuple(value_tuple))
                return result['last_id']

            else:
                # 有log_id则更新
                update_params = {
                    'id': log_id,
                    'result': params['result']
                }
                fields = [
                    'result = %s'
                ]
                condition = ' id = %s '
                value_tuple = (update_params['result'], update_params['id'])
                return model.update('tbl_thirdpart_connection_logs', {
                    model.sql_constants.FIELDS: fields,
                    model.sql_constants.CONDITION: condition
                }, value_tuple)
        except Exception, e:
            logger.error('HTTP.POST Exception: %s, path: %s, method: %s, params: %s' % (
                e, 'tools.httputils', 'write_log', params))
            return None

    @staticmethod
    def do_get_with_log(url, params={}):
        log_params = {
            'transfer_method': 'HTTP.do_get_with_log',
            'addr': url,
            'params': json.dumps({'params': params}),
        }
        log_id = HttpUtils.write_log(log_params)

        result = HttpUtils.do_get(url, params=params)

        if log_id:
            log_update_params = {
                'log_id': log_id,
                'result': result
            }
            HttpUtils.write_log(log_update_params)
        return result

    @staticmethod
    def do_post_with_log(url, params={}, headers={}):
        """
        发送post请求
        :param url:
        :param params:
        :return:
        """
        # 记录传入参数
        log_params = {
            'transfer_method': 'HTTP.do_post_with_log',
            'addr': url,
            'params': json.dumps({'params': params,
                                  'headers': headers}),
        }
        log_id = HttpUtils.write_log(log_params)

        result = HttpUtils.do_post(url, params=params, headers=headers)
        # 记录结果
        if log_id:
            log_update_params = {
                'log_id': log_id,
                'result': result
            }
            HttpUtils.write_log(log_update_params)
        return result

    @staticmethod
    def do_post_with_cert_with_log(url, params={}, headers={}, client_key=None, client_cert=None):
        """
        :param url:
        :param params:
        :param headers:
        :param client_key:
        :param client_cert:
        :return:
        """
        # 记录传入参数
        log_params = {
            'transfer_method': 'HTTP.do_post_with_cert_with_log',
            'addr': url,
            'params': json.dumps({'params': params,
                                  'headers': headers,
                                  'client_key': client_key,
                                  'client_cert': client_cert}),
        }
        log_id = HttpUtils.write_log(log_params)
        result = HttpUtils.do_post_with_cert(url, params=params, headers=headers, client_key=client_key,
                                             client_cert=client_cert)
        # 记录结果
        if log_id:
            log_update_params = {
                'log_id': log_id,
                'result': result
            }
            HttpUtils.write_log(log_update_params)
        return result

    @staticmethod
    @tornado.gen.coroutine
    def write_log_asyn(params):
        """
        写入日志
        :param params:
        :return:
        """
        try:
            # gen模块需要raise来返回结果，使用try捕捉异常会将结果抛进except Exception中，而不会直接返回
            result_data = None

            log_id = params.get('log_id', '')
            model = ModelBase()
            logger = Logs().logger

            if not log_id:
                path = ''
                method = ''
                stack_back = inspect.currentframe()
                for i in range(len(inspect.stack())):
                    stack_back = stack_back.f_back

                    if stack_back and stack_back.f_locals.get('service_path', ''):
                        path = stack_back.f_locals.get('service_path', '')
                        method = stack_back.f_locals.get('method', '')
                        break
                insert_params = {
                    'transfer_method': params['transfer_method'],
                    'addr': params['addr'],
                    'path': path,
                    'method': method,
                    'params': params['params'],
                    'result': '',
                }
                # 没有log_id则插入
                key = 'transfer_method, addr, path, method, params, result'
                val = '%s, %s, %s, %s, %s, %s'
                value_tuple = (insert_params['transfer_method'], insert_params['addr'], insert_params['path'],
                               insert_params['method'], insert_params['params'], insert_params['result'])

                result = model.insert('tbl_thirdpart_connection_logs', {
                    model.sql_constants.KEY: key,
                    model.sql_constants.VAL: val
                }, tuple(value_tuple))
                result_data = result['last_id']
                raise Exception()

            else:
                # 有log_id则更新
                update_params = {
                    'id': log_id,
                    'result': params['result']
                }
                fields = [
                    'result = %s'
                ]
                condition = ' id = %s '
                value_tuple = (update_params['result'], update_params['id'])
                result = model.update('tbl_thirdpart_connection_logs', {
                    model.sql_constants.FIELDS: fields,
                    model.sql_constants.CONDITION: condition
                }, value_tuple)
                result_data = result
                raise Exception()
        except Exception, e:
            if result_data is None and log_id:
                logger.error('HTTP.POST Exception: %s, path: %s, method: %s, params: %s' % (
                    e, 'tools.httputils', 'write_log_asyn', params))
            raise tornado.gen.Return(result_data)

    @staticmethod
    @tornado.gen.coroutine
    def get_with_log(url, params={}):
        log_params = {
            'transfer_method': 'HTTP.do_get_with_log',
            'addr': url,
            'params': json.dumps({'params': params}),
        }

        log_id = yield HttpUtils.write_log_asyn(log_params)

        result = HttpUtils.do_get(url, params=params)

        if log_id:
            log_update_params = {
                'log_id': log_id,
                'result': result
            }
            yield HttpUtils.write_log_asyn(log_update_params)
        raise tornado.gen.Return(result)

    @staticmethod
    @tornado.gen.coroutine
    def post_with_log(url, params={}, headers={}):
        # 记录参数
        log_params = {
            'transfer_method': 'HTTP.post_with_log',
            'addr': url,
            'params': json.dumps({'params': params,
                                  'headers': headers}),
        }
        log_id = yield HttpUtils.write_log_asyn(log_params)

        result = yield HttpUtils.post(url, params=params, headers=headers)

        # 记录结果
        if log_id:
            log_update_params = {
                'log_id': log_id,
                'result': result
            }
            yield HttpUtils.write_log_asyn(log_update_params)

        raise tornado.gen.Return(result)

if __name__ == '__main__':
    from base.service import ServiceBase
    s = ServiceBase()
    s.httputils.do_get_with_log('https://www.baidu.com')
