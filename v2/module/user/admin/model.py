# -*- coding:utf-8 -*-
"""
@author: zzx
@file: model.py
@time: 2017/9/7 17:29
"""

import tornado.gen
from source.async_model import AsyncModelBase


class Model(AsyncModelBase):
    @tornado.gen.coroutine
    def create_admin(self, params):
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
            if admin_data is None:
                raise Exception('sql error')

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
            admin_key = 'admin_id, shop_id, admin_power'
            admin_val = '%s,%s,%s'
            admin_value_tuple = (admin_data['last_id'], params['shop_id'], params['admin_power'])
            admin_result = yield self.insert('tbl_um_shop_admin', {self.sql_constants.KEY: admin_key,
                                                                   self.sql_constants.VAL: admin_val},
                                             tuple(admin_value_tuple),
                                             auto_commit=False)

            if admin_result is None:
                raise Exception('sql error')
            yield self.tx.commit()
            result = self.sql_constants.SUCCESS
        except Exception, e:
            print Exception, ':', e
            yield self.tx.rollback()
        raise self._gr(result)

    @tornado.gen.coroutine
    def create_exist_admin(self, params):
        admin_key = 'admin_id, shop_id, admin_power'
        admin_val = '%s,%s,%s'
        admin_value_tuple = (params['admin_id'], params['shop_id'], params['admin_power'])
        admin_result = yield self.insert('tbl_um_shop_admin', {self.sql_constants.KEY: admin_key,
                                                               self.sql_constants.VAL: admin_val},
                                         tuple(admin_value_tuple))
        raise self._gr(admin_result)

    @tornado.gen.coroutine
    def update_power(self, params):

        """
        更新权限
        :param params:
        :return:
        """
        # 需要更新的区域
        fields = []
        # 查询条件
        condition = ''
        value_list = []

        if 'admin_power' in params:
            fields.append('admin_power = %s ')
            value_list.append(params['admin_power'])

        condition += ' admin_id = %s and'
        value_list.append(params['admin_id'])

        condition += ' shop_id = %s'
        value_list.append(params['shop_id'])

        result = yield self.update('tbl_um_shop_admin', {self.sql_constants.FIELDS: fields,
                                                         self.sql_constants.CONDITION: condition}, tuple(value_list))
        raise self._gr(result)

    @tornado.gen.coroutine
    def query_admin_all(self, params):
        """
        更新权限
        :param params:
        :return:
        """
        # 请求字段
        fields = []
        # 查询条件
        condition = ' 1 = 1 '
        # 查询的值
        value_list = []

        if 'shop_id' in params:
            condition += ' and shop_id = %s '
            value_list.append(params['shop_id'])
        if 'admin_id' in params:
            condition += ' and admin_id = %s '
            value_list.append(params['admin_id'])

        result = yield self.find('tbl_um_shop_admin', {
            self.sql_constants.FIELDS: fields,
            self.sql_constants.CONDITION: condition
        }, tuple(value_list), 'list')
        raise self._gr(result)

    @tornado.gen.coroutine
    def delete_admin(self, params):
        """
        删除管理员
        :param params: 
        :return: 
        """
        condition = ' admin_id = %s and shop_id = %s '
        value_tuple = (params['admin_id'], params['shop_id'])
        result = yield self.delete('tbl_um_shop_admin', {self.sql_constants.CONDITION: condition},
                                   value_tuple)
        raise self._gr(result)
