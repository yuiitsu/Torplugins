# -*- coding:utf-8 -*-

"""
退出登录
@author onlyfu
@time 2017/8/30
"""
import tornado.gen
from base.base import Base


class Controller(Base):

    auth = (('admin', 'seller'), 'post')

    def initialize(self):
        Base.initialize(self)

    @tornado.gen.coroutine
    def post(self):
        self.do_service('user.auth.service', 'quit', {
            'token': self.get_cookie('token')
        })

        self.clear_cookie('token')
        self.out(self._e('SUCCESS'))