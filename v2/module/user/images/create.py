# -*- coding:utf-8 -*-

"""
@author: delu
@file: create.py
@time: 17/5/16 上午11:46
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
        res = yield self.do_service('library.images.service', 'create_image', params=params)
        self.out(res)
