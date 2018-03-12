# -*- coding:utf-8 -*-

"""
@author: zzx
@file: user.details
@time: 17/7/5
用户详细信息
"""
import tornado.gen
from v1.base.base import Base


class Controller(Base):
    auth = (('admin', 'seller'), 'post')
    userService = None

    def initialize(self):
        Base.initialize(self)

    @tornado.gen.coroutine
    def post(self):
        # yield Base.post(self)
        params = {
            'nick_name': self.params('nick_name'),
            'real_name': self.params('real_name'),
            'company': self.params('company'),
            'admin_id': self.user_data['admin_id']
        }

        res = yield self.do_service('user.details.service', 'create', params=params)

        self.out(res)
