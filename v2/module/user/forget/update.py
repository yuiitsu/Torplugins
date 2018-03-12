# -*- coding:utf-8 -*-

"""
@author: zzx
@time: 17/7/7
忘记密码
"""
import tornado.gen
from v1.base.base import Base


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
            'account': self.params('account')
        }

        res = yield self.do_service('user.forget.service', 'update_forget_password', params)

        self.out(res)



