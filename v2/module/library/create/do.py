# -*- coding:utf-8 -*-

"""
@author: xhb
@time: 2017/11/22 13:32
"""
from base.base import Base
import tornado.gen


class Controller(Base):

    auth = True

    @tornado.gen.coroutine
    def post(self):
        params = self.params()
        params['admin_id'] = self.user_data['admin_id']
        res = yield self.do_service('library.category.service', 'create_category', params=params)
        self.out(res)
