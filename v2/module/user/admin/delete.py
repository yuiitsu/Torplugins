# -*- coding:utf-8 -*-

"""
@author: zzx
@file: delete.py
@time: 2017/9/8 9:10
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
            'shop_id': self.user_data['shop_id'],
            'account': self.params('username'),
            # 'shop_id': 7
        }

        res = yield self.do_service('user.admin.service', 'delete_admin', params)

        self.out(res)
