# -*- coding:utf-8 -*-

"""
@author: delu
@file: httputils.py
@time: 17/5/2 上午10:36
"""
import urllib
import urllib.request
import urllib.parse
import json
import tornado.gen
from tornado.httpclient import HTTPRequest
from tornado.httpclient import AsyncHTTPClient
from tornado.httpclient import HTTPClient
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
        logger.info('发送请求 url: %s, params : ', url, params)
        url_params = '?'
        if len(params) > 0:
            params = urllib.parse.urlencode(params)
            url += url_params + params
            # for key in params:
            #     url_params += '%s=%s&' % (key, params[key])
            # url += url_params + 'x=1'

        req = urllib.request.urlopen(url)
        # res_data = urllib.request.urlopen(req)
        res = req.read()
        logger.info('请求结果 %s', res)
        return res

    @staticmethod
    def do_post(url, params={}, headers={}, is_json=False, timeout=10):
        """
        发送post请求
        :param url: 
        :param params: 
        :return: 
        """
        logger.info('发送请求 url: %s, params: %s', url, json.dumps(params))
        params_urlencode = params if isinstance(params, str) else urllib.parse.urlencode(params)

        if headers:
            req = urllib.request.Request(url=url, data=params_urlencode, headers=headers)
        else:
            req = urllib.request.Request(url=url, data=params_urlencode)

        res_data = urllib.request.urlopen(req, timeout=timeout)
        return_data = res_data.read()
        logger.info('请求结果 %s', return_data)
        if isinstance(return_data, bytes):
            return_data = return_data.decode(encoding='utf-8', errors='ignore')
        if is_json:
            try:
                return_data = json.loads(return_data)
            except Exception as e:
                logger.exception('JSON ERROR', e)
        return return_data

    @staticmethod
    def do_put(url, params={}, headers={}, is_json=False):
        """
        发送put请求
        :param url: 
        :param params: 
        :return: 
        """
        logger.info('发送请求 url: %s, params: %s', url, json.dumps(params))
        params_urlencode = params if isinstance(params, str) else urllib.parse.urlencode(params)
        if headers:
            req = urllib.request.Request(url=url, data=params_urlencode, headers=headers)
        else:
            req = urllib.request.Request(url=url, data=params_urlencode)

        req.get_method = lambda: 'PUT'
        res_data = urllib.request.urlopen(req, timeout=10)
        res = res_data.read()
        logger.info('请求结果 %s', res)
        if is_json:
            try:
                res = json.loads(res)
            except Exception as e:
                logger.exception('JSON ERROR', e)
        return res

    @staticmethod
    def do_post_with_cert(url, params={}, headers={}, client_key=None, client_cert=None):
        body = params if isinstance(params, str) else urllib.parse.urlencode(params)
        http_request = HTTPRequest(url, 'POST', body=body, headers=headers, validate_cert=False, client_key=client_key,
                                   client_cert=client_cert)
        http_client = HTTPClient()
        fetch_result = http_client.fetch(http_request)
        return fetch_result.body

    @staticmethod
    @tornado.gen.coroutine
    def get(url, params={}, headers={}, is_json=False):
        if params:
            url = url + '?' + urllib.parse.urlencode(params)
        # if len(params) > 0:
        #     for key in params:
        #         # 字符串(中文)进行encode
        #         url_params += '%s=%s&' % (key, params[key])
        #     # 删除最后的&
        #     url = (url + url_params)[:-1]

        http_request = HTTPRequest(url, 'GET', headers=headers, validate_cert=False)
        http_client = AsyncHTTPClient()
        return_data = None
        try:
            fetch_result = yield http_client.fetch(http_request)
            return_data = fetch_result.body
        except Exception as e:
            logger.info("HTTP GET RESULT: %s",  return_data)
            logger.exception(e)
            raise e
        final_result = HttpUtils.able_decode(return_data)
        if final_result:
            return_data = final_result

        if is_json and final_result:
            try:
                return_data = json.loads(return_data.replace('\r\n', ''))
            except Exception as e:
                logger.exception('json error', e)

        raise tornado.gen.Return(return_data)

    @staticmethod
    @tornado.gen.coroutine
    def get_status(url, params={}, headers={}, is_json=False):
        if params:
            url = url + '?' + urllib.parse.urlencode(params)
        # if len(params) > 0:
        #     for key in params:
        #         # 字符串(中文)进行encode
        #         url_params += '%s=%s&' % (key, params[key])
        #     # 删除最后的&
        #     url = (url + url_params)[:-1]

        http_request = HTTPRequest(url, 'GET', headers=headers, validate_cert=False)
        http_client = AsyncHTTPClient()
        try:
            fetch_result = yield http_client.fetch(http_request)
        except Exception as e:
            logger.exception(e)
            raise e

        raise tornado.gen.Return(fetch_result)

    @staticmethod
    @tornado.gen.coroutine
    def post(url, params={}, headers={}, is_json=False, need_log=True, request_type='POST', auth_username='', auth_password='', need_cookie=False):
        logger.info('url: %s, params: %s', url, params)
        body = params if isinstance(params, str) else urllib.parse.urlencode(params)
        if request_type != 'POST':
            body = None
        http_request = HTTPRequest(url, request_type, body=body, headers=headers, validate_cert=False, auth_username=auth_username, auth_password=auth_password)
        http_client = AsyncHTTPClient()
        return_data = None
        response_headers = None
        try:
            fetch_result = yield http_client.fetch(http_request)
            if need_cookie:
                response_headers = fetch_result.headers

            return_data = fetch_result.body
        except Exception as e:
            logger.info("HTTP POST RESULT: %s",  return_data)
            logger.exception(e)
            raise e
        final_result = HttpUtils.able_decode(return_data)
        if final_result:
            return_data = final_result

        if is_json and final_result:
            try:
                return_data = json.loads(return_data.replace('\r\n', ''))

                if need_cookie:
                    return_data['response_headers'] = response_headers
            except Exception as e:
                logger.exception('json error', e)
        if need_log:
            logger.info('response: %s', return_data)
        raise tornado.gen.Return(return_data)

    @staticmethod
    @tornado.gen.coroutine
    def post_status(url, params={}, headers={}, is_json=False, need_log=True, request_type='POST',
                    auth_username='', auth_password=''):
        logger.info('url: %s, params: %s', url, params)
        body = params if isinstance(params, str) else urllib.parse.urlencode(params)
        if request_type != 'POST':
            body = None

        http_request = HTTPRequest(url, request_type, body=body, headers=headers, validate_cert=False,
                                   auth_username=auth_username, auth_password=auth_password)
        http_client = AsyncHTTPClient()
        try:
            fetch_result = yield http_client.fetch(http_request)
            return_data = fetch_result.body
        except Exception as e:
            logger.exception(e)
            raise e

        if need_log:
            logger.info('response: %s', return_data)

        raise tornado.gen.Return(fetch_result)

    @staticmethod
    @tornado.gen.coroutine
    def post_with_cert(url, params={}, headers={}, client_key=None, client_cert=None):
        body = params if isinstance(params, str) else urllib.parse.urlencode(params)
        http_request = HTTPRequest(url, 'POST', body=body, headers=headers, validate_cert=False, client_key=client_key,
                                   client_cert=client_cert)
        http_client = AsyncHTTPClient()
        fetch_result = yield http_client.fetch(http_request)
        raise tornado.gen.Return(fetch_result.body)

    @staticmethod
    def able_decode(bytes_str):
        """
        判断bytes_str能否被utf-8编码
        :param bytes_str: 
        :return: 
        """
        try:
            if isinstance(bytes_str, bytes):
                return bytes_str.decode('utf-8')
            else:
                return False
        except Exception as e:
            return False


if __name__ == '__main__':
    # from tornado.ioloop import IOLoop
    #
    # def handle_response(response):
    #     if response.error:
    #         print("Error: %s" % response.error)
    #     else:
    #         print(response.body)
    #
    #
    # http_client = AsyncHTTPClient()
    # http_client.fetch("http://www.google.com/", handle_response)
    # IOLoop.current().start()

    import requests
    url = 'http://www.google.com'
    res = requests.get(url)
    print(res.text)
