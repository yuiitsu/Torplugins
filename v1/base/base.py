#!usr/bin/env python
# -*- coding:utf-8 -*-

import hashlib
import json
import random
import time

import tornado.gen

import conf.config as config
from constants.cachekey_predix import CacheKeyPredix
from constants.constants import Constants
from constants.error_code import Code
from source.controller import Controller
from source.properties import Properties
from source.redisbase import RedisBase
# from source.async_redis import AsyncRedis
from source.service_manager import ServiceManager as serviceManager
from tools.common_util import CommonUtil
from tools.date_json_encoder import CJsonEncoder
from tools.logs import Logs


class Base(Controller):

    json = json
    time = time
    logged_user = {}
    redis = RedisBase()
    # redis = AsyncRedis()
    user_data = {}
    buyer_user_data = {}
    version = config.CONF['version']
    cache_key_pre = CacheKeyPredix
    error_code = Code
    constants = Constants
    properties = Properties()
    logger = Logs().logger
    auth = None
    shop_id = '0'
    _params = {}

    # def initialize(self):
    #     """
    #     初始化
    #     初始化数据类
    #     """
    #     # Controller.config = config.CONF
    #     # Controller.initialize(self)
    #     # # self.view_data['title'] = self.config['title']
    #     # # 访问者身份标识
    #     # self.get_user_unique_code()
    #     # self._params = self.get_params()

    @tornado.gen.coroutine
    def prepare(self):
        """
        接受请求前置方法
            1.解析域名
            2.权限检查
        :return:
        """
        # 访问者身份标识
        self.get_user_unique_code()
        self._params = self.get_params()

        yield self.get_shop_host(self.request.host)
        if self.auth:
            if self.auth[0] is not None:
                auth_status = yield self.auth_check()
                if not auth_status:
                    self.finish()

                # 刷新token
                yield self.refresh_token()

    @tornado.gen.coroutine
    def auth_check(self):
        """ 
        登录认证
            根据控制器的权限设置，调用不同的权限检查
        """

        auth = self.auth
        # 如果没有设置权限，返回
        if not auth or not auth[0]:
            raise self._gr(True)

        is_auth_error = False
        is_login = True
        is_auth = True
        power_group = auth[0]
        for group in power_group:
            if group == 'buyer':
                # 买家
                buyer_token = self.params('buyer_token')
                if not buyer_token:
                    buyer_token = self.get_cookie('buyer_token')

                if not buyer_token:
                    is_login = False
                    break

                cache_key = self.cache_key_pre.BUYER_TOKEN + self.md5(buyer_token)
                user_data = self.redis.hgetall(cache_key)
                self.buyer_user_data = user_data

            elif group == 'admin' or group == 'seller':
                sign = self.params('sign')
                if sign:
                    sign_token = yield self.sign_login()
                    if not sign_token:
                        token = self.params('token')
                        if not token:
                            token = self.get_cookie('token')

                        if not token:
                            is_login = False
                            break
                    else:
                        token = sign_token
                else:
                    token = self.params('token')
                    if not token:
                        token = self.get_cookie('token')

                    if not token:
                        is_login = False
                        break

                cache_key = self.cache_key_pre.ADMIN_TOKEN + self.md5(token)
                user_data = self.redis.hgetall(cache_key)
                self.user_data = user_data

            else:
                is_auth_error = True
                self.logger.exception('auth error')
                break

            if not user_data:
                is_login = False
                break

            if 'user_type' not in user_data:
                is_login = False
                break

            if user_data['user_type'] not in self.auth[0]:
                is_auth = False
                break

        if is_auth_error:
            self.error_out(self._e('AUTH_SET_ERROR'))
            raise self._gr(False)

        if not is_login:
            self.error_out(self._e('NOT_LOGIN'))
            raise self._gr(False)

        if not is_auth:
            self.error_out(self._e('AUTH_ERROR'))
            raise self._gr(False)

        raise self._gr(True)

    @tornado.gen.coroutine
    def create_token(self, params, user_type, expire=None):
        """
        创建token和cookie
        :param params:
        :param user_type:
        :param expire:
        :return:
        """
        if not user_type:
            raise self._gr({'code': -1, 'msg': ''})

        # 处理domain
        request = self.request
        host = request.host
        host_port = host.split(':')
        hosts = host_port[0].split('.')
        domain_base = '.'.join(hosts[-2:])

        # 根据用户类型，生成缓存KEY
        if user_type == 'admin':
            token = self.cache_key_pre.ADMIN_TOKEN + self.salt(salt_len=32)
            cache_key = self.cache_key_pre.ADMIN_TOKEN + self.md5(token)
            expire = expire if expire else int(self.properties.get('expire', 'ADMIN_EXPIRE'))
            cookie_key = 'token'
            params['user_type'] = self.constants.ADMIN_TYPE
        elif user_type == 'buyer':
            token = self.cache_key_pre.BUYER_TOKEN + self.salt(salt_len=32)
            cache_key = self.cache_key_pre.BUYER_TOKEN + self.md5(token)
            expire = expire if expire else int(self.properties.get('expire', 'BUYER_EXPIRE'))
            cookie_key = 'buyer_token'
            params['user_type'] = self.constants.BUYER_TYPE
        else:
            raise self._gr({'code': -1, 'msg': ''})

        # 创建缓存
        self.redis.hmset(cache_key, params)

        # 设置cookie
        if 'remember' in params and params['remember'] == '1':
            self.redis.expire(cache_key, int(self.properties.get('expire', 'ADMIN_EXPIRE_REMEMBER')))
            self.set_cookie(cookie_key, token,
                            expires=time.time() + int(self.properties.get('expire', 'ADMIN_EXPIRE_REMEMBER')),
                            domain=domain_base)
        else:
            self.redis.expire(cache_key, expire)
            self.set_cookie(cookie_key, token, domain=domain_base)

        raise self._gr({'token': token})

    @tornado.gen.coroutine
    def refresh_token(self):
        """
        刷新token
        :return:
        """
        auth = self.auth
        # 如果没有设置权限，返回
        if not auth or not auth[0]:
            raise self._gr(True)

        cache_key = ''
        expire = ''
        refresh_expire = ''
        power_group = auth[0]
        for group in power_group:
            if group == 'buyer':
                # 买家
                buyer_token = self.params('buyer_token')
                if not buyer_token:
                    buyer_token = self.get_cookie('buyer_token')

                if not buyer_token:
                    break

                cache_key = self.cache_key_pre.BUYER_TOKEN + self.md5(buyer_token)
                expire = int(self.properties.get('expire', 'BUYER_EXPIRE'))
                refresh_expire = int(self.properties.get('expire', 'BUYER_REFRESH_EXPIRE'))
            elif group == 'admin' or group == 'seller':
                token = self.params('token')
                if not token:
                    token = self.get_cookie('token')

                if not token:
                    break

                if self.params('sign'):
                    shop_id = self.params('shop_id')
                    token = 'sign:' + shop_id
                    # cache_key = self.cache_key_pre.ADMIN_TOKEN + self.md5(token)

                cache_key = self.cache_key_pre.ADMIN_TOKEN + self.md5(token)
                expire = int(self.properties.get('expire', 'ADMIN_EXPIRE'))
                refresh_expire = int(self.properties.get('expire', 'ADMIN_REFRESH_EXPIRE'))

        if cache_key and expire and refresh_expire:
            cache_data = self.redis.ttl(cache_key)
            if cache_data:
                left_seconds = int(cache_data)
                # 获取用户登录数据
                self.user_data = self.redis.hgetall(cache_key)
                if (expire - left_seconds) >= refresh_expire:
                    # 如果token的总生命秒数 － 剩余生命秒数 <= 刷新秒数，则重新设置token的生命秒数
                    self.redis.expire(cache_key, expire)

    @tornado.gen.coroutine
    def sign_login(self):
        """
        签名登录
            1.检查缓存是否有值，有值直接返回真
            2.如果没值，调用验签服务进行验签
            3.验签通过，生成缓存
        :return:
        """
        # 检查缓存是否有值
        shop_id = self.params('shop_id')
        token = 'sign:' + shop_id
        cache_key = self.cache_key_pre.ADMIN_TOKEN + self.md5(token)
        user_data = self.redis.hgetall(cache_key)
        if user_data:
            raise self._gr(token)

        sign = self.params('sign')
        sing_result = yield self.do_service('user.auth.sign.service', 'sign_login', self.params())
        if sing_result['code'] != 0:
            raise self._gr(False)

        # 创建缓存
        self._params['sign'] = sign
        self.redis.hmset(cache_key, {
            'shop_id': shop_id,
            'user_type': self.constants.SELLER_TYPE,
            'admin_id': -1,
            'group_id': 0
        })

        # 设置cookie
        expire = int(self.properties.get('expire', 'ADMIN_EXPIRE'))
        self.redis.expire(cache_key, expire)

        raise self._gr(token)

    def md5(self, text):
        """ 
        MD5加密
        @:param text 需加密字符串
        @return 加密后字符串
        """
        result = hashlib.md5(text)
        return result.hexdigest()

    def create_uuid(self):
        """
        声称随机字符串
        :return: 
        """
        m = hashlib.md5()
        m.update(bytes(str(time.time()), encoding='utf-8'))
        return m.hexdigest()

    def sha1(self, text):
        """ 
        sha1 加密
        @:param text 需加密字符串
        @return 加密后字符串
        """
        return hashlib.sha1(text).hexdigest()

    def salt(self, salt_len=6, is_num=False):
        """ 
        密码加密字符串
        生成一个固定位数的随机字符串，包含0-9a-z
        @:param salt_len 生成字符串长度
        """

        if is_num:
            chrset = '0123456789'
        else:
            chrset = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWSYZ'
        salt = []
        for i in range(salt_len):
            item = random.choice(chrset)
            salt.append(item)

        return ''.join(salt)

    def out(self, data):
        """ 
        输出结果
        :param code: 错误信息对象
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

    def clear_template_cache(self):
        """ 清除模板缓存
        """

        self._template_loaders.clear()

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

    @tornado.gen.coroutine
    def get_shop_host(self, host):
        """
        根据二级域名获取店铺ID
        规则：
        只有当有二级域名，且不为www时执行查找，先从缓存中获取，再从数据库中获取
        :param host:
        :return:
        """
        is_use_domain = 'False'
        try:
            is_use_domain = self.properties.get('domain', 'is_use')
        except Exception, e:
            print e
        if host and cmp(is_use_domain, 'True') == 0:
            hosts = host.split('.')
            if len(hosts) > 1 and cmp(hosts[0], 'www') != 0 and cmp(hosts[0], 'wxauth') != 0:
                second_domain = hosts[0]
                if second_domain:
                    # 获取缓存中的数据
                    cache_key = self.cache_key_pre.DOAMIN_SHOP_ID + second_domain
                    shop_id = self.redis.get(cache_key)
                    if not shop_id:
                        # 获取数据库中的数据
                        result = yield self.do_service('channel.shop.service', 'query_shop_id', {
                            'domain': second_domain
                        })
                        if result and result['code'] == 0:
                            shop_id = result['data']['shop_id']
                            # 设置缓存数据
                            self.redis.set(cache_key, shop_id, 604800)
                    else:
                        # 获取缓存剩余过期秒数，如果小于3天，则重新设置过期时间
                        expire_second = self.redis.ttl(cache_key)
                        if int(expire_second) <= 10800:
                            self.redis.expire(cache_key, 604800)

                    if shop_id:
                        self.shop_id = shop_id
                        # 给参数对象添加shop_id
                        # params = self.params()
                    self._params['shop_id'] = shop_id

    def do_service(self, service_path, method, params={}):
        """
        调用服务
        :param service_path: 
        :param method: 
        :param params: 
        :return: 
        """
        token = self.get_cookie('token')
        buyer_token = self.get_cookie('buyer_token')
        language = self.get_cookie('language')
        if not token:
            token = self.params('token')
        if not buyer_token:
            buyer_token = self.params('buyer_token')
        if not language:
            language = self.params('language')

        # params['token'] = token if token else ''
        # params['buyer_token'] = buyer_token if buyer_token else ''
        # params['language'] = language if language else 'cn'
        return serviceManager.do_service(service_path, method, params=params, version=config.CONF['version'])

    def get_user_unique_code(self):
        """
        创建访问者唯一身份标识
        :return:
        """
        cookie_name = 'unique_code'
        unique_code = self.get_cookie(cookie_name)
        if not unique_code or len(unique_code) != 32:
            unique_code = self.salt(32)
            self.set_cookie(cookie_name, unique_code)
        return unique_code

    def _e(self, error_key):
        """
        :param error_key:
        :return: 
        """
        language = self.get_cookie('language')
        if not language:
            language = self.params('language')
        language = language if language else 'cn'
        language_module = self.importlib.import_module('language.' + language).Code
        data = {}
        for key in self.error_code[error_key]:
            data[key] = self.error_code[error_key][key]
        if error_key in language_module:
            data['msg'] = language_module[error_key]

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
        return {
            'user_unique_code': self.get_user_unique_code(),
            'remote_ip': ip,
            'user_agent': request.headers['User-Agent']
        }


if __name__ == '__main__':
    print time.time()
