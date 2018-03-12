# -*- coding:utf-8 -*-

"""
@author: delu
@file: update.py
@time: 17/5/22 下午7:40
"""
from base.base import Base
import tornado.gen


class Controller(Base):
    auth = (('admin', 'seller'), 'post')

    def initialize(self):
        Base.initialize(self)

    @tornado.gen.coroutine
    def post(self):
        # yield Base.post(self)
        params = self.params()
        params['admin_id'] = self.user_data['admin_id']
        res = yield self.do_service('user.password.service', 'update_password', params=params)
        self.out(res)
