# -*- coding:utf-8 -*-

"""
@author onlyfu
@time 2017/8/30
"""
import tornado.gen
from base.service import ServiceBase


class Service(ServiceBase):
    """
    user_service
    """

    user_model = None

    def __init__(self):
        """
        对象初始化方法
        添加你需要使用的model
        格式 项目model文件夹下的文件名或者 包名1.包名2.文件名 (无.py后缀)
        """
        self.user_model = self.import_model('user.model')

    @tornado.gen.coroutine
    def query_user_account_one(self, params):
        """
        获取单个帐号信息
        :param params:
        :return:
        """
        if self.common_utils.is_empty(['account'], params) and self.common_utils.is_empty(['admin_id'], params):
            raise self._gre('PARAMS_NOT_EXIST')

        account_result = yield self.user_model.query_user_account_one(params)
        if not account_result:
            raise self._gre('DATA_NOT_EXIST')

        raise self._grs(account_result)

    @tornado.gen.coroutine
    def query_user_one(self, params):
        """
        查询管理员
        :param params:
        :return:
        """
        data = yield self.user_model.query_user_one(params)

        if data is None:
            raise self._gre('SQL_EXECUTE_ERROR')
        else:
            result = self._e('SUCCESS')
            result['data'] = data
            raise self._gr(result)
