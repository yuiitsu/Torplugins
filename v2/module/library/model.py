# -*- coding:utf-8 -*-

"""
@author xhb
@time 2017/11/8
"""
import tornado.gen
from source.async_model import AsyncModelBase


class Model(AsyncModelBase):
    @tornado.gen.coroutine
    def create_category(self, params):
        """
        创建目录
        :param params:
        :return:
        """
        key = 'category_name, admin_id'
        val = '%s, %s'
        value_tuple = (params['category_name'], params['admin_id'])
        result = yield self.insert('tbl_lb_category', {
            self.sql_constants.KEY: key,
            self.sql_constants.VAL: val,
        }, value_tuple)
        raise self._gr(result)

    @tornado.gen.coroutine
    def update_category(self, params):
        """
        更新category名字
        :param params:
        :return:
        """
        fields = ['category_name=%s']
        condition = ' category_id=%s '
        value_tuple = (params['category_name'], params['category_id'])

        result = yield self.update('tbl_lb_category', {
            self.sql_constants.FIELDS: fields,
            self.sql_constants.CONDITION: condition
        }, value_tuple)

        raise self._gr(result)

    @tornado.gen.coroutine
    def delete_category(self, params):
        value_list = []
        condition = 'category_id' + self.build_in(len(params['category_id_list'])) + 'and admin_id = %s'
        value_list.extend(params['category_id_list'])
        value_list.append(params['admin_id'])
        result = yield self.delete('tbl_lb_category', {
            self.sql_constants.CONDITION: condition,
        }, tuple(value_list))
        raise self._gr(result)

    @tornado.gen.coroutine
    def query_list(self, params):
        """
        查询目录列表
        :param params:
        :return:
        """
        fields = []
        condition = ' 1 = 1'
        value_list = []
        limit = []
        if 'page_index' in params and 'page_size' in params:
            limit.append(str(params['page_index']))
            limit.append(str(params['page_size']))
        if 'admin_id' in params:
            condition += ' and admin_id = %s '
            value_list.append(params['admin_id'])
        order = ' create_time desc '

        result = yield self.page_find('tbl_lb_category', {
            self.sql_constants.FIELDS: fields,
            self.sql_constants.CONDITION: condition,
            self.sql_constants.LIMIT: limit,
            self.sql_constants.ORDER: order
        }, tuple(value_list))

        raise self._gr(result)
