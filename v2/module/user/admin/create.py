# -*- coding:utf-8 -*-

"""
@author: zzx
@file: create.py
@time: 2017/9/7 17:18
"""
from base.base import Base
import tornado.gen


import tornado.gen
from base.base import Base


class Controller(Base):
    auth = (('admin', 'seller'), 'post')

    def initialize(self):
        Base.initialize(self)

    @tornado.gen.coroutine
    def post(self):
        # yield Base.post(self)
        params = {
            'verify_code': self.params('verify_code'),
            'password': self.params('password'),
            'check_password': self.params('check_password'),
            'account': self.params('username'),
            'shop_id': self.user_data['shop_id'],
            # 'shop_id': 7,
            'admin_power': self.params('admin_power')
        }

        res = yield self.do_service('user.admin.service', 'create', params)

        self.out(res)
