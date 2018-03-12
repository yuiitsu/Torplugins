# -*- coding:utf-8 -*-

"""
@author: zzx
@file: service.py
@time: 17/7/5
"""
import tornado.gen
from v1.base.service import ServiceBase


class Service(ServiceBase):


    user_model = None

    def __init__(self):
        """
        对象初始化方法
        添加你需要使用的model
        格式 项目model文件夹下的文件名或者 包名1.包名2.文件名 (无.py后缀)
        """
        self.user_model = self.import_model('user.model.user_model')

    @tornado.gen.coroutine
    def create(self, params):
        """
        添加用户详细信息
        :param params: 
        :return: 
        """
        if self.common_utils.is_empty(['nick_name', 'real_name', 'company', 'admin_id'], params):
            # 必要参数非空
            raise self._gre('PARAMS_NOT_EXIST')

        res = yield self.user_model.create_details(params)

        if res is None:
            raise self._gre('SQL_EXECUTE_ERROR')
        else:
            raise self._gre('SUCCESS')


