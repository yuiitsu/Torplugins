# -*- coding:utf-8 -*-

"""
@author: zzx
@file: update.py
@time: 17/7/4
"""
import tornado.gen
from base.base import Base


class Controller(Base):

    auth = (('seller',), 'post')

    def initialize(self):
        Base.initialize(self)

    @tornado.gen.coroutine
    def post(self):
        # yield Base.post(self)
        params = self.params()
        params['shop_id'] = self.user_data['shop_id']

        res = yield self.do_service('user.init.service', 'init_dm', params=params)
        self.out(res)

