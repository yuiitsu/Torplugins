# -*- coding:utf-8 -*-

"""
@author: zzx
@file: service.py
@time: 17/7/10
"""
import tornado.gen
from v1.base.service import ServiceBase


class Service(ServiceBase):
    """
    verify_service
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
    def update_forget_password(self, params):
        """
        找回密码
        :param params:
        :return:
        """
        if self.common_utils.is_empty(['account', 'verify_code', 'password', 'check_password'], params):
            # 必要参数非空
            raise self._gre('PARAMS_NOT_EXIST')

        # 确认密码和密码不匹配
        if cmp(params['password'], params['check_password']) != 0:
            raise self._gre('PASSWORD_NOT_MATCH')

        # 账号已存在
        account = yield self.user_model.query_user_account_one(params)
        if not account:
            raise self._gre('DATA_NOT_EXIST')

        # 验证验证码是否正确
        verify_code_cache_key = self.cache_key_predix.VERIFY_CODE + params['account']
        if params['verify_code'].lower() != self.redis.get(verify_code_cache_key):
            raise self._gre('THIRD_PART_VERIFY_CODE_FAILED')
        else:
            self.redis.delete(verify_code_cache_key)

        salt = self.salt()
        password = self.md5(self.md5(params['password']) + salt)

        params['password'] = password
        params['salt'] = salt

        res = yield self.user_model.update_password(params)

        if res is None:
            raise self._gre('SQL_EXECUTE_ERROR')
        else:
            raise self._gre('SUCCESS')