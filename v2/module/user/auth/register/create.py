# -*- coding:utf-8 -*-

"""
@author onlyfu
@time 2017/8/30
"""
import tornado.gen
from base.base import Base


class Controller(Base):
    auth = (None, 'post')
    userService = None

    def initialize(self):
        Base.initialize(self)

    @tornado.gen.coroutine
    def post(self):
        # yield Base.post(self)
        params = {
            'verify_code': self.params('verify_code'),
            'password': self.params('password'),
            'check_password': self.params('check_password'),
            'account': self.params('username')
        }

        res = yield self.do_service('user.auth.register.service', 'create', params)

        self.out(res)