# -*- coding:utf-8 -*-

"""
@author onlyfu
@time 2017/6/8
"""
import tornado.gen
from base.base import Base


class Controller(Base):

    goods_service = None
    auth = (('admin', 'seller'), 'get')

    def initialize(self):
        Base.initialize(self)

    @tornado.gen.coroutine
    def get(self):
        # 获取参数
        # yield Base.get(self)
        params = {
            'shop_id': self.user_data['shop_id'],
            'page_index': self.params('page_index') if self.params('page_index') else '1',
            'page_size': self.params('page_size') if self.params('page_size') else '100',
            'key': self.params('key') if self.params('key') else ''
        }
        result = yield self.do_service('customer.service', 'query_list', params)
        self.out(result)
