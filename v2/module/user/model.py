# -*- coding:utf-8 -*-

"""
@author onlyfu
@time 2017/8/30
"""
import tornado.gen
from source.async_model import AsyncModelBase


class Model(AsyncModelBase):

    @tornado.gen.coroutine
    def create_user(self, params):
        """
        创建
        :param params:
        :return:
        """
        result = None
        try:
            user_key = 'nick_name'
            user_val = '%s'
            user_value_tuple = (params['account'],)
            admin_data = yield self.insert('tbl_um_admin', {self.sql_constants.KEY: user_key,
                                                            self.sql_constants.VAL: user_val},
                                           user_value_tuple,
                                           auto_commit=False)

            account_key = 'admin_id, account, password, salt'
            account_val = '%s,%s,%s,%s'
            account_value_tuple = (admin_data['last_id'], params['account'], params['password'],
                                   params['salt'])
            sql_result = yield self.insert('tbl_um_adminaccount', {self.sql_constants.KEY: account_key,
                                                                   self.sql_constants.VAL: account_val},
                                           account_value_tuple,
                                           auto_commit=False)
            if sql_result is None:
                raise Exception('sql error')
            yield self.tx.commit()
            result = self.sql_constants.SUCCESS
        except Exception, e:
            print Exception, ':', e
            yield self.tx.rollback()
        raise self._gr(result)

    @tornado.gen.coroutine
    def query_user_account_one(self, params):
        """
        获取一条帐号数据
        :param params:
        :return:
        """
        # 请求字段
        fields = []
        # 查询条件
        condition = ' 1 = 1 '
        # 查询的值
        value_list = []

        if 'account' in params and params['account']:
            condition += ' and account = %s '
            value_list.append(params['account'])

        if 'admin_id' in params and params['admin_id']:
            condition += ' and admin_id = %s '
            value_list.append(params['admin_id'])

        result = yield self.find('tbl_um_adminaccount', {
            self.sql_constants.FIELDS: fields,
            self.sql_constants.CONDITION: condition
        }, tuple(value_list))

        raise self._gr(result)

    @tornado.gen.coroutine
    def query_user_one(self, params):
        """
        查询管理员基本信息
        :param params:
        :return:
        """
        # 请求字段
        fields = []
        # 查询条件
        condition = ' 1 = 1 '
        # 查询的值
        value_list = []

        if 'admin_id' in params:
            condition += ' and admin_id = %s '
            value_list.append(params['admin_id'])

        result = yield self.find('tbl_um_admin', {
            self.sql_constants.FIELDS: fields,
            self.sql_constants.CONDITION: condition
        }, tuple(value_list))

        raise self._gr(result)

    @tornado.gen.coroutine
    def update_password(self, params):

        """
        更新密码
        :param params:
        :return:
        """
        # 需要更新的区域
        fields = []
        # 查询条件
        condition = ''
        value_list = []

        if 'password' in params:
            fields.append('password = %s ')
            value_list.append(params['password'])
        if 'salt' in params:
            fields.append(' salt = %s ')
            value_list.append(params['salt'])

        condition += ' account = %s'
        value_list.append(params['account'])

        result = yield self.update('tbl_um_adminaccount', {self.sql_constants.FIELDS: fields,
                                                    self.sql_constants.CONDITION: condition}, tuple(value_list))
        raise self._gr(result)