#!usr/bin/env python
# -*- coding:utf-8 -*-

import hashlib
import json
import random
import string
import time

import tornado.gen
from tornado.web import Finish

import conf.config as config
from constants.cachekey_predix import CacheKeyPredix
from constants.constants import Constants
from constants.error_code import Code
from source.controller import Controller
from source.properties import properties as properties
from source.redisbase import RedisBase
from source.async_redis import AsyncRedis
from source.service_manager import ServiceManager as serviceManager
from tools.common_util import CommonUtil
from tools.date_json_encoder import CJsonEncoder


class Base(Controller):
    """ 基类
    """
    json = json
    time = time
    logged_user = {}
    redis = RedisBase()
    #redis = AsyncRedis()
    user_data = {}
    buyer_user_data = {}
    version = config.CONF['version']
    cache_key_predix = CacheKeyPredix
    error_code = Code
    constants = Constants
    properties = properties
    auth = None
    shop_id = '0'
    language_code = {}
    _params = {}

    # def initialize(self):
    #     """
    #     初始化
    #     初始化数据类
    #     """
    #     Controller.config = config.CONF
    #     Controller.initialize(self)
    #     # self.view_data['title'] = self.config['title']
    #     # 访问者身份标识
    #     self.get_user_unique_code()
    #     self._params = self.get_params()

    @tornado.gen.coroutine
    def auth_second(self):
        """ 
        登录认证
        读取cookie值，判断是否具有权限

        @params strUserName string 用户名
        """
        token = self.get_cookie('token')
        buyer_token = self.get_cookie('buyer_token')
        super_token = self.get_cookie('super_token')

        if not buyer_token:
            buyer_token = self.params('buyer_token')
        if not token:
            token = self.params('token')
        if not super_token:
            super_token = self.params('super_token')

        admin_login = False
        if super_token:
            cache_key = self.cache_key_predix.SUPERADMIN_TOKEN + self.md5(super_token)
            super_admin_data = self.redis.hgetall(cache_key)
            if super_admin_data:
                self.super_admin_data = super_admin_data
                if 'user_type' in super_admin_data:
                    admin_login = True
                    if not self.auth[0] or super_admin_data['user_type'] in self.auth[0] \
                            or super_admin_data['user_type'] == 'super_admin':
                        raise self._gr(True)

        if token:
            cache_key = self.cache_key_predix.ADMIN_TOKEN + self.md5(token)
            user_data = self.redis.hgetall(cache_key)
            if user_data:
                self.user_data = user_data
                if 'user_type' in user_data:
                    admin_login = True
                    if not self.auth[0] or user_data['user_type'] in self.auth[0] \
                            or user_data['user_type'] == 'super_admin':
                        raise self._gr(True)

        if buyer_token:
            buyer_cache_key = self.cache_key_predix.BUYER_TOKEN + self.md5(buyer_token)
            user_data = self.redis.hgetall(buyer_cache_key)
            if user_data:
                self.user_data = user_data
                shop_id = self.params('shop_id')
                if cmp(str(shop_id), str(self.user_data['shop_id'])) != 0 and shop_id:
                    self.error_out(self._e('NOT_LOGIN'))
                    raise self._gr(False)

                if 'user_type' in user_data:
                    admin_login = True
                    if not self.auth[0] or user_data['user_type'] in self.auth[0] \
                            or user_data['user_type'] == 'super_admin':
                        raise self._gr(True)

        # 只要有一种账户登录了，就是权限不足
        if admin_login:
            self.error_out(self._e('AUTH_ERROR'))
        else:
            self.error_out(self._e('NOT_LOGIN'))
        raise self._gr(False)

    def auth_request(self, request_type):
        """
        请求类型检查
        :param request_type: 请求类型
        :return: 
        """
        if not self.auth[1] or request_type.lower() in self.auth:
            return True

        return False

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

    def create_random_text(self, number):
        """
        创建随机定长字符串
        :param number: 
        :return: 
        """
        salt = ''.join(random.sample(string.ascii_letters + string.digits, number))

        return salt

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
        :param data: 返回数据字典
        """
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(self.json.dumps(data, cls=CJsonEncoder))

    def error_out(self, error, data):
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
    def prepare(self):
        # 访问者身份标识
        self.get_user_unique_code()
        self._params = self.get_params()

        yield self.get_shop_host(self.request.host)
        if self.auth:
            if self.auth[0] is not None:
                auth_status = yield self.auth_second()
                if not auth_status:
                    # Finish()
                    self.finish()

            # if not self.auth_request(self.request.method):
            #     self.error_out(self._e('REQUEST_TYPE_ERROR'))
            #     # Finish()
            #     self.finish()

        # 刷新token
        yield self.refresh_token()

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
                    cache_key = self.cache_key_predix.DOAMIN_SHOP_ID + second_domain
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

        params['token'] = token if token else ''
        params['buyer_token'] = buyer_token if buyer_token else ''
        params['language'] = language if language else 'cn'
        return serviceManager.do_service(service_path, method, params=params, version=config.CONF['version'])

    @tornado.gen.coroutine
    def create_cookie_and_token(self, params={}):
        """
        创建cookie 和 token 记录用户登录信息
        :param params: 
        :return: 
        """
        params = CommonUtil.remove_element(params, ['salt', 'password'])

        admin_token = self.cache_key_predix.ADMIN_TOKEN + self.salt(salt_len=32)
        cache_key = self.cache_key_predix.ADMIN_TOKEN + self.md5(admin_token)
        # 新增
        params['user_type'] = self.constants.ADMIN_TYPE
        self.redis.hmset(cache_key, params)
        if params['remember'] == '1':
            self.redis.expire(cache_key, int(self.properties.get('expire', 'ADMIN_EXPIRE_REMEMBER')))
            self.set_cookie('token', admin_token,
                            expires=time.time() + int(self.properties.get('expire', 'ADMIN_EXPIRE_REMEMBER')))
        else:
            self.redis.expire(cache_key, int(self.properties.get('expire', 'ADMIN_EXPIRE')))
            self.set_cookie('token', admin_token)

        print 'token: %s, cache_key: %s' % (admin_token, cache_key)
        raise self._gr({'token': admin_token})

    @tornado.gen.coroutine
    def update_cookie_and_token(self, params={}):
        """
        更新cookie 和 token 记录用户登录信息
        :param params: 
        :return: 
        """

        token = self.get_cookie('token')
        if not token:
            token = self.params('token')
        cache_key = self.cache_key_predix.ADMIN_TOKEN + self.md5(token)
        cache_value = self.redis.hgetall(cache_key)
        if 'shop_id' in params:
            cache_value['shop_id'] = params['shop_id']
            cache_value['user_type'] = self.constants.SELLER_TYPE
            self.redis.delete(cache_key)
            self.redis.hmset(cache_key, cache_value)
            if params['remember'] == '1':
                self.redis.expire(cache_key, int(self.properties.get('expire', 'ADMIN_EXPIRE_REMEMBER')))
                self.set_cookie('token', token,
                                expires=time.time() + int(self.properties.get('expire', 'ADMIN_EXPIRE_REMEMBER')))
            else:
                self.redis.expire(cache_key, int(self.properties.get('expire', 'ADMIN_EXPIRE')))
                self.set_cookie('token', token)

    @tornado.gen.coroutine
    def create_cookie_and_token_for_buyer(self, params={}):
        """
        创建cookie 和 token 记录买家登录信息
        :param params: 
        :return: 
        """
        params = CommonUtil.remove_element(params, ['password', 'salt'])
        buyer_token = self.cache_key_predix.BUYER_TOKEN + self.salt(salt_len=32)
        buyer_cache_key = self.cache_key_predix.BUYER_TOKEN + self.md5(buyer_token)
        # 新增
        params['user_type'] = self.constants.BUYER_TYPE
        self.redis.hmset(buyer_cache_key, params)
        if 'scen_type' in params and params['scen_type'] == self.constants.SCEN_TYPE_WECHAT:
            # 如果是微信登录，则采用微信过期时间, 默认两个小时
            if 'expire' not in params or not params['expire']:
                params['expire'] = 7200
            self.redis.expire(buyer_cache_key, params['expire'])
            self.set_cookie('buyer_token', buyer_token)
        else:
            self.redis.expire(buyer_cache_key, int(self.properties.get('expire', 'BUYER_EXPIRE')))
            self.set_cookie('buyer_token', buyer_token)
        raise self._gr({'buyer_token': buyer_token, 'buyer_id': params['buyer_id']})

    @tornado.gen.coroutine
    def create_cookie_and_token_for_superadmin(self, params={}):
        """
        创建cookie 和 token 记录平台管理员登录信息
        token和cookie的有效时间策略和admin一致，不记住是两小时，记住是七天
        @auth Fern9
        :param params:
        :return:
        """
        params = CommonUtil.remove_element(params, ['salt', 'password'])

        superadmin_token = self.cache_key_predix.SUPERADMIN_TOKEN + self.salt(salt_len=32)
        cache_key = self.cache_key_predix.SUPERADMIN_TOKEN + self.md5(superadmin_token)
        # 新增
        params['user_type'] = self.constants.SUPER_ADMIN_TYPE
        self.redis.hmset(cache_key, params)
        if params['remember'] == '1':
            self.redis.expire(cache_key, int(self.properties.get('expire', 'ADMIN_EXPIRE_REMEMBER')))
            self.set_cookie('super_token', superadmin_token,
                            expires=time.time() + int(self.properties.get('expire', 'ADMIN_EXPIRE_REMEMBER')))
        else:
            self.redis.expire(cache_key, int(self.properties.get('expire', 'ADMIN_EXPIRE')))
            self.set_cookie('super_token', superadmin_token)
        print 'token: %s, cache_key: %s' % (superadmin_token, cache_key)
        raise self._gr({'token': superadmin_token})

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

    @tornado.gen.coroutine
    def quit_shop(self):
        """
        店铺管理员退出
        :param params: 
        :return: 
        """
        token = self.get_cookie('token')
        if not token:
            token = self.params('token')
        cache_key = self.cache_key_predix.ADMIN_TOKEN + self.md5(token)
        cache_value = self.redis.hgetall(cache_key)
        cache_value = CommonUtil.remove_element(cache_value, ['shop_id'])
        cache_value['user_type'] = self.constants.ADMIN_TYPE
        self.redis.delete(cache_key)
        self.redis.hmset(cache_key, cache_value, int(self.properties.get('expire', 'ADMIN_EXPIRE')))
        # redis.expire(cache_key, int(self.properties.get('expire', 'ADMIN_EXPIRE')))

    @tornado.gen.coroutine
    def refresh_token(self):
        """
        刷新token
        :return: 
        """
        token = self.get_cookie('token')
        buyer_token = self.get_cookie('buyer_token')
        # 平台管理员token
        super_token = self.get_cookie('super_token')
        if not token:
            token = self.params('token')
        if not buyer_token:
            buyer_token = self.params('buyer_token')
        if not super_token:
            super_token = self.params('super_token')

        if token:
            cache_key = self.cache_key_predix.ADMIN_TOKEN + self.md5(token)
            cache_data = self.redis.ttl(cache_key)
            if cache_data:
                left_seconds = int(cache_data)
                # 获取用户登录数据
                self.user_data = self.redis.hgetall(cache_key)
                if (int(self.properties.get('expire', 'ADMIN_EXPIRE')) - left_seconds) >= \
                        int(self.properties.get('expire', 'ADMIN_REFRESH_EXPIRE')):
                    # 如果token的总生命秒数 － 剩余生命秒数 <= 刷新秒数，则重新设置token的生命秒数
                    self.redis.expire(cache_key, int(self.properties.get('expire', 'ADMIN_EXPIRE')))

        if buyer_token:
            buyer_cache_key = self.cache_key_predix.BUYER_TOKEN + self.md5(buyer_token)
            cache_data = self.redis.ttl(buyer_cache_key)
            if cache_data:
                left_seconds = int(cache_data)
                # 获取用户登录数据
                self.buyer_user_data = self.redis.hgetall(buyer_cache_key)
                if (int(self.properties.get('expire', 'BUYER_EXPIRE')) - left_seconds) >= \
                        int(self.properties.get('expire', 'BUYER_REFRESH_EXPIRE')):
                    # 如果token的总生命秒数 － 剩余生命秒数 <= 刷新秒数，则重新设置token的生命秒数
                    self.redis.expire(buyer_cache_key, int(self.properties.get('expire', 'BUYER_EXPIRE')))

        if super_token:
            cache_key = self.cache_key_predix.SUPERADMIN_TOKEN + self.md5(super_token)
            cache_data = self.redis.ttl(cache_key)
            if cache_data:
                left_seconds = int(cache_data)
                # 获取平台管理员登录数据
                self.super_admin_data = self.redis.hgetall(cache_key)
                if (int(self.properties.get('expire', 'ADMIN_EXPIRE')) - left_seconds) >= \
                        int(self.properties.get('expire', 'ADMIN_REFRESH_EXPIRE')):
                    # 如果token的总生命秒数 － 剩余生命秒数 <= 刷新秒数，则重新设置token的生命秒数
                    self.redis.expire(cache_key, int(self.properties.get('expire', 'ADMIN_EXPIRE')))

    @tornado.gen.coroutine
    def delete_super_admin_token(self):
        """
        @auth Fern9
        删除平台管理员token
        :return:
        """
        token = self.get_cookie('super_token')
        if not token:
            token = self.params('super_token')
        if token:
            cache_key = self.cache_key_predix.SUPERADMIN_TOKEN + self.md5(token)
            self.redis.delete(cache_key)
            self.clear_cookie('super_token')

    def _e(self, error_key):
        """
        :param error_key:
        :return:
        """
        data = {}
        for key in self.error_code[error_key]:
            data[key] = self.error_code[error_key][key]
        if error_key in self.language_code:
            data['msg'] = self.language_code[error_key]

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
