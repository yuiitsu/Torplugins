# -*- coding:utf-8 -*-

"""
@author: onlyfu
@time: 20/04/17
"""
from base.base import Base
import tornado.gen


class Controller(Base):

    auth = (('buyer',), False)

    @tornado.gen.coroutine
    def post(self):
        params = self.params()
        params['buyer_id'] = self.buyer_user_data['buyer_id']
        res = yield self.do_service('buyer.service', 'update_buyer', params=params)
        self.out(res)
