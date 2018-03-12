# -*- coding:utf-8 -*-

"""
@author: yuiitsu
@time: 2017/11/21 17:57
"""
from base.base import Base
import tornado.gen


class Controller(Base):

    auth = (('seller',), 'post')

    # def initialize(self):
    #     Base.initialize(self)

    @tornado.gen.coroutine
    def post(self):
        params = self.params()
        params['shop_id'] = self.user_data['shop_id']
        params['admin_id'] = self.user_data['admin_id']
        res = yield self.do_service('goods.brand.service', 'create', params)
        self.out(res)
