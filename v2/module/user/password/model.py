# -*- coding:utf-8 -*-

"""
@author onlyfu
@time 2017/8/30
"""
import tornado.gen
from source.async_model import AsyncModelBase


class Model(AsyncModelBase):

    @tornado.gen.coroutine
    def update_password(self, params):
        """
        更新管理员密码
        :param params:
        :return:
        """
        fields = ['password = %s']
        condition = ' account_id = %s '
        value_tuple = (params['password'], params['account_id'])
        result = yield self.update('tbl_um_adminaccount', {self.sql_constants.FIELDS: fields,
                                                           self.sql_constants.CONDITION: condition},
                                   value_tuple)
        raise self._gr(result)