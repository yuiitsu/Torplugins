# -*- coding:utf-8 -*-

"""
@author: zzx
@file: update.py
@time: 2017/9/7 18:42
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
        params = {
            'account': self.params('username'),
            'shop_id': self.user_data['shop_id'],
            # 'shop_id': 7,
            'admin_power': self.params('admin_power')
        }

        res = yield self.do_service('user.admin.service', 'update_power', params)

        self.out(res)
