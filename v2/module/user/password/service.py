# -*- coding:utf-8 -*-

"""
@author onlyfu
@time 2017/8/30
"""
import tornado.gen
from module.user.service import Service as UserService


class Service(UserService):

    password_model = None

    def __init__(self):
        """
        对象初始化方法
        添加你需要使用的model
        格式 项目model文件夹下的文件名或者 包名1.包名2.文件名 (无.py后缀)
        """
        super(Service, self).__init__()
        self.password_model = self.import_model('user.password.model')

    @tornado.gen.coroutine
    def update_password(self, params={}):

        if self.common_utils.is_empty(['admin_id', 'password', 're_password', 'old_password'], params):
            raise self._gre('PARAMS_NOT_EXIST')

        if cmp(params['password'], params['re_password']) != 0:
            raise self._gre('PASSWORD_NOT_MATCH')

        # 根据admin_id获取帐户信息
        account_result = yield self.query_user_account_one(params)
        if not account_result or account_result['code'] != 0:
            raise self._gre('DATA_NOT_EXIST')
        account = account_result['data']

        # 验证密码是否正确
        old_password = self.md5(self.md5(params['old_password']) + account['salt'])
        if cmp(account['password'], old_password) != 0:
            raise self._gre('PASSWORD_ERROR')

        # 修改密码
        params['password'] = self.md5(self.md5(params['password']) + account['salt'])
        params['account_id'] = account['account_id']
        result = yield self.password_model.update_password(params)
        if result:
            raise self._gre('SUCCESS')
        else:
            raise self._gre('SQL_EXECUTE_ERROR')