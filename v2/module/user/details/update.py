# -*- coding:utf-8 -*-

"""
@author: delu
@file: update.py
@time: 17/4/24 下午2:19
"""
import tornado.gen
from v1.base.base import Base


class Controller(Base):
    auth = (('admin', 'seller'), 'post')

    def initialize(self):
        Base.initialize(self)

    @tornado.gen.coroutine
    def post(self):
        # yield Base.post(self)
        params = {
            'admin_id': self.user_data['admin_id'],
            'nick_name': self.params('nick_name'),
            'mobile_no': self.params('mobile_no'),
            'qq_account': self.params('qq_account'),
            'email_address': self.params('email_address')
        }
        res = yield self.do_service('user.service.user_service', 'update', params=params)
        self.out(res)

