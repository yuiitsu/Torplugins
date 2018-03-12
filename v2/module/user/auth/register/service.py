# -*- coding:utf-8 -*-

"""
@author onlyfu
@time 2017/8/30
"""
import tornado.gen
from v1.base.service import ServiceBase


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
    def create(self, params):
        """
        注册管理员
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
        admin_nums = yield self.user_model.query_user_account_one(params)
        if admin_nums:
            raise self._gre('DATA_EXIST')

        code = self.redis.get(self.cache_key_predix.VERIFY_CODE + params['account'])
        if params['verify_code'].lower() != code:
            raise self._gre('THIRD_PART_VERIFY_CODE_FAILED')
        else:
            self.redis.delete(self.cache_key_predix.VERIFY_CODE + params['account'])

        salt = self.salt()
        password = self.md5(self.md5(params['password']) + salt)

        params['password'] = password
        params['salt'] = salt

        res = yield self.user_model.create_user(params)

        if res is None:
            raise self._gre('SQL_EXECUTE_ERROR')
        else:
            raise self._gre('SUCCESS')

    @tornado.gen.coroutine
    def query_user_account_one(self, params):
        result = yield self.user_model.query_user_account_one(params)
        raise self._gr(result)
