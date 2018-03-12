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
    def login(self, params):
        """
        管理员登录
        :param params:
        :return:
        """
        if self.common_utils.is_empty(['account', 'password'], params):
            raise self._gre('PARAMS_NOT_EXIST')

        # 查询账户信息
        user_account = yield self.user_model.query_user_account_one(params)
        if user_account is None:
            raise self._gre('DATA_NOT_EXIST')

        if cmp(self.md5(self.md5(params['password']) + user_account['salt']), user_account['password']) == 0:

            # 登录成功
            # 生成cookie和服务端token
            result = self._e('SUCCESS')
            result['data'] = user_account
            raise self._gr(result)

        else:
            raise self._gre('PASSWORD_ERROR')