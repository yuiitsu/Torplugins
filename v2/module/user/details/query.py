# -*- coding:utf-8 -*-

"""
获取帐户信息
@author onlyfu
@time 2017/8/30
"""
import tornado.gen
from base.base import Base


class Controller(Base):

    auth = (None, 'get')
    userService = None

    def initialize(self):
        Base.initialize(self)

    @tornado.gen.coroutine
    def post(self):
        # yield Base.post(self)
        params = {
            'account': self.params('username')
        }

        res = yield self.do_service('user.service', 'query_user_account_one', params)

        self.out(res)
