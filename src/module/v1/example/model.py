# -*- coding:utf-8 -*-

"""
@author onlyfu
@time 2017/8/31
"""
import tornado.gen
from source.async_model import AsyncModelBase


class Model(AsyncModelBase):

    @tornado.gen.coroutine
    def update_buyer_account(self, params):
        """
        更新买家账号信息
        :param params: 
        :return: 
        """

        sql_list = []

        # 买家账户表更新
        account_fields = [
            'shop_id=%s'
        ]
        account_condition = ' shop_id = %s and account = %s '
        account_value_list = [params['shop_id']]

        if 'scene_id' in params and params['scene_id']:
            account_fields.append('scene_id=%s')
            account_value_list.append(params['scene_id'])

        if 'union_id' in params and params['union_id']:
            account_fields.append('union_id=%s')
            account_value_list.append(params['union_id'])

        account_value_list.append(params['shop_id'])
        account_value_list.append(params['buyer_id'])

        sql_list.append({
            self.sql_constants.SQL_TYPE: self.sql_constants.UPDATE,
            self.sql_constants.TABLE_NAME: 'tbl_um_buyer_account',
            self.sql_constants.DICT_DATA: {
                self.sql_constants.FIELDS: account_fields,
                self.sql_constants.CONDITION: account_condition
            },
            self.sql_constants.VALUE_TUPLE: tuple(account_value_list)
        })

        # 买家表更新
        buyer_fields = [
            'shop_id=%s'
        ]
        buyer_condition = ' shop_id = %s and buyer_id = %s '
        buyer_value_list = [params['shop_id']]

        if 'scene_id' in params and params['scene_id']:
            buyer_fields.append('scene_id=%s')
            buyer_value_list.append(params['scene_id'])

        buyer_value_list.append(params['shop_id'])
        buyer_value_list.append(params['buyer_id'])

        sql_list.append({
            self.sql_constants.SQL_TYPE: self.sql_constants.UPDATE,
            self.sql_constants.TABLE_NAME: 'tbl_um_buyer',
            self.sql_constants.DICT_DATA: {
                self.sql_constants.FIELDS: buyer_fields,
                self.sql_constants.CONDITION: buyer_condition
            },
            self.sql_constants.VALUE_TUPLE: tuple(buyer_value_list)
        })

        result = yield self.do_sqls(sql_list)

        raise self._gr(result)

    @tornado.gen.coroutine
    def query_buyer_count(self, params):
        """
        查询买家数量
        """
        # 查询条件
        condition = ' 1 = 1 '
        # 查询的值
        value_list = []
        if 'mobile_no' in params and params['mobile_no']:
            condition += ' and mobile_no = %s '
            value_list.append(params['mobile_no'])
        if 'buyer_id' in params and params['buyer_id']:
            condition += ' and buyer_id = %s '
            value_list.append(params['buyer_id'])

        result = yield self.get_rows('tbl_um_buyer', {self.sql_constants.CONDITION: condition}, tuple(value_list))
        raise self._gr(result)

    @tornado.gen.coroutine
    def query_buyer(self, params):
        """
        查询买家基本信息
        :param params:
        :return:
        """
        # 查询字段
        fields = [
            'account.account',
            'account.shop_id',
            'account.buyer_id',
            'account.type',
            'account.bind_buyer_id',
            'account.password',
            'account.salt',
            'buyer.scene_type',
            'buyer.origin',
            'buyer.name',
            'buyer.head_img',
            'buyer.mobile',
            'buyer.email'
        ]
        # 查询条件
        condition = ' account.shop_id = %s '
        # 查询的值
        value_tuple = [params['shop_id']]

        if params.get('mobile'):
            condition += ' and buyer.mobile = %s '
            value_tuple.append(params['mobile'])
        if params.get('email'):
            condition += ' and buyer.email= %s '
            value_tuple.append(params['email'])
        if params.get('buyer_id'):
            condition += ' and account.buyer_id= %s '
            value_tuple.append(params['buyer_id'])

        join = [{self.sql_constants.TABLE_NAME: 'tbl_um_buyer as buyer',
                 self.sql_constants.JOIN_CONDITION: 'buyer.buyer_id = account.buyer_id and buyer.shop_id = account.shop_id'},
                ]

        result = yield self.find('tbl_um_buyer_account as account', {
            self.sql_constants.FIELDS: fields,
            self.sql_constants.CONDITION: condition,
            self.sql_constants.JOIN: join
        }, value_tuple)

        raise self._gr(result)

    @tornado.gen.coroutine
    def query_buyer_by_mobile(self, params):
        """
        查询买家基本信息
        :param params:
        :return:
        """
        # 查询字段
        fields = []
        # 查询条件
        condition = ' mobile = %s and shop_id = %s'
        # 查询的值
        value_tuple = (params['mobile'], params['shop_id'])

        result = yield self.find('tbl_um_buyer', {
            self.sql_constants.FIELDS: fields,
            self.sql_constants.CONDITION: condition
        }, value_tuple)

        raise self._gr(result)

    @tornado.gen.coroutine
    def query_buyer_by_account(self, params):
        """
        查询买家基本信息
        :param params:
        :return:
        """
        # 查询字段
        fields = [
            'account.account',
            'account.shop_id',
            'account.buyer_id',
            'account.type',
            'account.bind_buyer_id',
            'account.password',
            'account.salt',
            'account.union_id',
            'buyer.scene_type',
            'buyer.origin',
            'buyer.name',
            'buyer.head_img',
            'buyer.mobile',
            'buyer.email'
        ]
        # 查询条件
        condition = ' account.account = %s and account.shop_id = %s'
        # 查询的值
        value_tuple = (params['account'], params['shop_id'])

        join = [{self.sql_constants.TABLE_NAME: 'tbl_um_buyer as buyer',
                 self.sql_constants.JOIN_CONDITION: 'buyer.buyer_id = account.buyer_id and buyer.shop_id = account.shop_id'},
                ]

        result = yield self.find('tbl_um_buyer_account as account', {
            self.sql_constants.FIELDS: fields,
            self.sql_constants.CONDITION: condition,
            self.sql_constants.JOIN: join
        }, value_tuple)

        raise self._gr(result)

    @tornado.gen.coroutine
    def create_buyer(self, params):
        """
        创建买家并且绑定bind_buyer_id
        :param params:
        :return:
        """
        sql_list = []
        key = 'buyer_id, shop_id, account, type, scene_id, union_id, password, salt'
        val = '%s, %s, %s, %s, %s, %s'
        value_tuple = (
            params['buyer_id'],
            params['shop_id'],
            params['account'],
            params['type'],
            params.get('scene_id', ''),
            params.get('union_id', ''),
            params['password'],
            params['salt']
        )

        sql_list.append({
            self.sql_constants.SQL_TYPE: self.sql_constants.INSERT,
            self.sql_constants.TABLE_NAME: 'tbl_um_buyer_account',
            self.sql_constants.DICT_DATA: {
                self.sql_constants.KEY: key,
                self.sql_constants.VAL: val
            },
            self.sql_constants.VALUE_TUPLE: value_tuple
        })

        key = 'buyer_id, shop_id, scene_type, scene_id, origin'
        val = '%s, %s, %s, %s'
        value_tuple = [
            params['buyer_id'],
            params['shop_id'],
            params['scene_type'],
            params.get('scene_id', ''),
            params['origin'],
        ]
        if params.get('email'):
            key += ', email'
            val += ', %s'
            value_tuple.append(params['email'])
        if params.get('mobile'):
            key += ', mobile'
            val += ', %s'
            value_tuple.append(params['mobile'])
        duplicate_key = [
            'scene_type=%s',
            'origin=%s'
        ]
        value_tuple.extend([params['scene_type'], params['origin']])

        sql_list.append({
            self.sql_constants.SQL_TYPE: self.sql_constants.INSERT,
            self.sql_constants.TABLE_NAME: 'tbl_um_buyer',
            self.sql_constants.DICT_DATA: {
                self.sql_constants.KEY: key,
                self.sql_constants.VAL: val,
                self.sql_constants.DUPLICATE_KEY_UPDATE: duplicate_key
            },
            self.sql_constants.VALUE_TUPLE: value_tuple
        })

        # 更新bind_buyer_id
        # bind_fields = ['bind_buyer_id = %s']
        # bind_condition = ' mobile_no = %s and bind_buyer_id  <> %s'
        # bind_value_tuple = (params['bind_buyer_id'], params['mobile_no'], params['buyer_id'])
        # sql_list.append({
        #     self.sql_constants.SQL_TYPE: self.sql_constants.UPDATE,
        #     self.sql_constants.TABLE_NAME: 'tbl_um_buyer ',
        #     self.sql_constants.DICT_DATA: {
        #         self.sql_constants.FIELDS: bind_fields,
        #         self.sql_constants.CONDITION: bind_condition,
        #     },
        #     self.sql_constants.VALUE_TUPLE: bind_value_tuple
        # })
        result = yield self.do_sqls(sql_list)
        raise self._gr(result)

    @tornado.gen.coroutine
    def bind_mobile(self, params):
        """
        绑定手机号
        :param params:
        :return:
        """
        # 需要更新的区域
        fields = []
        # 查询条件
        condition = ''
        value_list = []

        if 'mobile_no' in params:
            fields.append(' mobile_no = %s ')
            value_list.append(params['mobile_no'])

        condition += ' buyer_id = %s'
        value_list.append(params['buyer_id'])

        result = yield self.update('tbl_um_buyer', {self.sql_constants.FIELDS: fields,
                                                    self.sql_constants.CONDITION: condition},
                                   tuple(value_list))
        raise self._gr(result)

    @tornado.gen.coroutine
    def query_bind(self, params):
        """
        查询买家基本信息
        :param params:
        :return:
        """
        # 查询字段
        fields = []
        # 查询条件
        condition = ' 1 = 1 '
        # 查询的值
        value_list = []

        if 'buyer_id' in params and params['buyer_id']:
            condition += ' and buyer_id = %s '
            value_list.append(params['buyer_id'])
        result = yield self.find('tbl_um_buyer', {self.sql_constants.FIELDS: fields,
                                                  self.sql_constants.CONDITION: condition}, tuple(value_list))
        raise self._gr(result)

    @tornado.gen.coroutine
    def update_buyer(self, params):
        """
        更新买家基本信息
        :param params: 
        :return: 
        """
        fields = []
        condition = ' buyer_id = %s and shop_id = %s '
        value_list = []
        if 'name' in params and params['name']:
            fields.append(' name = %s '),
            value_list.append(params['name'])
        if 'head_img' in params and params['head_img']:
            fields.append(' head_img = %s ')
            value_list.append(params['head_img'])
        value_list.append(params['buyer_id'])
        value_list.append(params['shop_id'])
        result = yield self.update('tbl_um_buyer', {self.sql_constants.FIELDS: fields,
                                                    self.sql_constants.CONDITION: condition},
                                   tuple(value_list))
        raise self._gr(result)

    @tornado.gen.coroutine
    def query_buyer_list(self, params):
        """
        查询买家列表
        :param params: 
        :return: 
        """
        condition = ' shop_id = %s '
        value_list = [params['shop_id']]
        if 'buyer_id_list' in params and params['buyer_id_list']:
            condition += ' and buyer_id ' + self.build_in(len(params['buyer_id_list']))
            value_list.extend(params['buyer_id_list'])
        result = yield self.find('tbl_um_buyer', {self.sql_constants.CONDITION: condition},
                                 tuple(value_list),
                                 self.sql_constants.LIST)
        raise self._gr(result)

    @tornado.gen.coroutine
    def query_bind_buyer(self, shop_id, bind_buyer_id):
        """
        通过绑定的buyer_id查询相关的账号信息
        :param bind_buyer_id:
        :return:
        """
        fields = ['buyer_id']
        condition = ' shop_id = %s and bind_buyer_id = %s'
        value_list = [shop_id, bind_buyer_id]
        result = yield self.find('tbl_um_buyer_account', {self.sql_constants.CONDITION: condition,
                                                          self.sql_constants.FIELDS: fields},
                                 tuple(value_list),
                                 self.sql_constants.LIST)
        raise self._gr(result)

    @tornado.gen.coroutine
    def bind_buyer_account(self, params):
        """
        绑定账户
        """
        sql_list = []
        fields = [
            'bind_buyer_id = %s',
            'channel=%s',
            'channel_create_time=%s'
        ]
        condition = ' account = %s and shop_id = %s '
        value_tuple = (
            params['bind_buyer_id'],
            params.get('channel', ''),
            self.date_utils.time_now(),
            params['account'], params['shop_id']
        )
        sql_list.append({
            self.sql_constants.SQL_TYPE: self.sql_constants.UPDATE,
            self.sql_constants.TABLE_NAME: 'tbl_um_buyer_account',
            self.sql_constants.DICT_DATA: {
                self.sql_constants.FIELDS: fields,
                self.sql_constants.CONDITION: condition
            }, self.sql_constants.VALUE_TUPLE: value_tuple
        })

        if params.get('mobile') or params.get('email'):
            buyer_field = []
            buyer_condition = ' buyer_id = %s and shop_id = %s '
            buyer_value = []
            if params.get('mobile'):
                buyer_field.append(' mobile = %s ')
                buyer_value.append(params['mobile'])
            if params.get('email'):
                buyer_field.append(' email = %s ')
                buyer_value.append(params['email'])

            buyer_value.extend([params['buyer_id'], params['shop_id']])
            sql_list.append({
                self.sql_constants.SQL_TYPE: self.sql_constants.UPDATE,
                self.sql_constants.TABLE_NAME: 'tbl_um_buyer',
                self.sql_constants.DICT_DATA: {
                    self.sql_constants.FIELDS: buyer_field,
                    self.sql_constants.CONDITION: buyer_condition,
                }, self.sql_constants.VALUE_TUPLE: tuple(buyer_value)
            })

        res = yield self.do_sqls(sql_list)

        raise self._gr(res)

    @tornado.gen.coroutine
    def query_main_account_list(self, params):
        """
        查询主账号信息
        :param params:
        :return:
        """
        # 查询字段
        fields = []
        # 查询条件
        condition = ' a1.shop_id = %s and a1.buyer_id ' + self.build_in(len(params['buyer_id_list']))
        # 查询的值
        value_tuple = [params['shop_id']]
        value_tuple.extend(params['buyer_id_list'])

        join = [{
            self.sql_constants.TABLE_NAME: 'tbl_um_buyer_account as a2',
            self.sql_constants.JOIN_CONDITION: 'a1.bind_buyer_id = a2.account'
        }]

        result = yield self.find('tbl_um_buyer_account as a1', {
            self.sql_constants.FIELDS: fields,
            self.sql_constants.CONDITION: condition,
            self.sql_constants.JOIN: join
        }, value_tuple, str_type=self.sql_constants.LIST)

        raise self._gr(result)
