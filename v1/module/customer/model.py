# -*- coding:utf-8 -*-

"""
@author onlyfu
@time 2017/6/8
"""
import tornado.gen
from source.async_model import AsyncModelBase


class Model(AsyncModelBase):

    @tornado.gen.coroutine
    def query_list(self, params):
        """
        查询客户列表
        :param params:
        :return:
        """
        # 请求字段
        fields = []
        # 请求条件
        condition = ' 1 = 1 '
        # 请求的值
        value_list = []

        if 'name' in params and params['name']:
            condition += " and name like %s"
            value_list.append('%' + params['name'] + '%')

        if 'mobile_no' in params and params['mobile_no']:
            condition += " and mobile_no = %s"
            value_list.append(params['mobile_no'])

        if 'key' in params and params['key']:
            condition += "and (name like %s or mobile_no = %s or email = %s)"
            value_list.append('%' + params['key'] + '%')
            value_list.append(params['key'])
            value_list.append(params['key'])

        condition += " and shop_id = %s "
        value_list.append(params['shop_id'])

        result = yield self.page_find('tbl_um_customer',
                                      {
                                          self.sql_constants.FIELDS: fields,
                                          self.sql_constants.CONDITION: condition,
                                          self.sql_constants.LIMIT: [str(params['page_index']),
                                                                     str(params['page_size'])],
                                          self.sql_constants.ORDER: 'create_time desc'
                                      },
                                      tuple(value_list)
                                      )
        raise self._gr(result)

    @tornado.gen.coroutine
    def dele(self, shop_id, customer_id_list):
        """
        删除客户
        :param shop_id:
        :param customer_id_list:
        :return:
        """
        condition = 'shop_id = %s and customer_id ' + self.build_in(len(customer_id_list))
        value_list = [shop_id]
        value_list.extend(customer_id_list)

        result = yield self.delete('tbl_um_customer', {
            self.sql_constants.CONDITION: condition
        }, tuple(value_list))

        raise self._gr(result)
