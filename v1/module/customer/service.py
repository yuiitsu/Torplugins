# -*- coding:utf-8 -*-

"""
@author onlyfu
@time 2017/6/8
"""
import tornado.gen
from v1.base.service import ServiceBase


class Service(ServiceBase):
    """
    user_service
    """

    model = None

    def __init__(self):
        """
        对象初始化方法
        添加你需要使用的model
        格式 项目model文件夹下的文件名或者 包名1.包名2.文件名 (无.py后缀)
        """
        self.model = self.import_model('user.customer.model')

    @tornado.gen.coroutine
    def query_list(self, params):
        """
        查询客户列表
        :param params:
        :return:
        """
        if 'shop_id' not in params or not params['shop_id']:
            raise self._gre('AUTH_ERROR')

        data = yield self.model.query_list(params)
        if data is None:
            raise self._gre('SQL_EXECUTE_ERROR')

        result = self._e('SUCCESS')
        result['data'] = data
        raise self._gr(result)

    @tornado.gen.coroutine
    def delete(self, params):
        """
        删除客户
        :param params:
        :return:
        """
        if 'shop_id' not in params or not params['shop_id']:
            raise self._gre('AUTH_ERROR')

        if 'customer_id' not in params or not params['customer_id']:
            raise self._gre('PARAMS_NOT_EXIST')

        data = yield self.model.dele(params['shop_id'], params['customer_id'].split(','))
        if data is None:
            raise self._gre('SQL_EXECUTE_ERROR')

        raise self._grs(data)
