# -*- coding:utf-8 -*-

"""
@author onlyfu
@time 2017/6/9
"""
import tornado.gen
from base.base import Base


class Controller(Base):

    goods_service = None
    auth = (('admin', 'seller'), 'post')

    def initialize(self):
        Base.initialize(self)

    @tornado.gen.coroutine
    def post(self):
        # 获取参数
        # yield Base.post(self)
        params = self.params()
        params['shop_id'] = self.user_data['shop_id']
        result = yield self.do_service('customer.service', 'delete', params)
        self.out(result)