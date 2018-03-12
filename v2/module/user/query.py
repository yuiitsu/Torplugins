# -*- coding:utf-8 -*-

"""
@author: delu
@file: query.py
@time: 17/4/24 下午2:01
"""
import tornado.gen
from v1.base.base import Base


class Controller(Base):
    auth = (('admin', 'seller'), 'get')

    def initialize(self):
        Base.initialize(self)

    @tornado.gen.coroutine
    def get(self):
        # yield Base.get(self)
        params = {
            'admin_id': self.user_data['admin_id']
        }
        # self.do_service(service_path, method_name, params)
        res = yield self.do_service('user.service', 'query_user_one', params)
        self.out(res)
