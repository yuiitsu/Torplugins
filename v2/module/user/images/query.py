# -*- coding:utf-8 -*-

"""
@author: delu
@file: query.py
@time: 17/5/16 上午11:46
"""
from base.base import Base
import tornado.gen


class Controller(Base):
    auth = (('admin', 'seller'), 'get')

    def initialize(self):
        Base.initialize(self)

    @tornado.gen.coroutine
    def get(self):
        # yield Base.get(self)
        params = {
            'admin_id': self.user_data['admin_id'],
            'page_index': self.params('page_index'),
            'page_size': self.params('page_size')
        }
        res = yield self.do_service('library.images.service', 'query_image_list', params=params)
        self.out(res)
