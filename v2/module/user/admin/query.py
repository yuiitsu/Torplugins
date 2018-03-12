# -*- coding:utf-8 -*-

"""
@author: zzx
@file: query.py
@time: 2017/9/7 19:08
"""
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
            'shop_id': self.user_data['shop_id'],
            # 'shop_id': 7
        }

        res = yield self.do_service('user.admin.service', 'query_admin_all', params)

        self.out(res)
