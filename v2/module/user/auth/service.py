# -*- coding:utf-8 -*-

"""
@author onlyfu
@time 2017/8/30
"""
import tornado.gen
from base.service import ServiceBase


class Service(ServiceBase):

    user_model = None

    def __init__(self):
        """
        对象初始化方法
        添加你需要使用的model
        格式 项目model文件夹下的文件名或者 包名1.包名2.文件名 (无.py后缀)
        """
        self.user_model = self.import_model('user.model')

    @tornado.gen.coroutine
    def quit(self, params):
        """
        退出登录
        :return:
        """
        if 'token' in params and params['token']:
            cache_key = self.cache_key_predix.ADMIN_TOKEN + self.md5(params['token'])
            self.redis.delete(cache_key)

        raise self._e('SUCCESS')
