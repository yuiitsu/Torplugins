# -*- coding:utf-8 -*-

"""
@author onlyfu
@time 2017/8/30
"""
import tornado.gen
from base.base import Base


class Controller(Base):

    # auth = (None, 'post')

    # def initialize(self):
    #     Base.initialize(self)

    @tornado.gen.coroutine
    def post(self):
        params = {
            'account': self.params('username'),
            'password': self.params('password'),
            'remember': self.params('remember')
        }
        result = yield self.do_service('user.auth.login.service', 'login', params)
        if result['code'] == 0:
            (result['data'])['remember'] = params['remember']
            yield self.create_cookie_and_token(result['data'])
        self.out(result)