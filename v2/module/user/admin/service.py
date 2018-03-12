# -*- coding:utf-8 -*-

"""
@author: zzx
@file: service.py
@time: 2017/9/7 17:20
"""
from base.service import ServiceBase
import tornado.gen


class Service(ServiceBase):
    """
    service
    """

    model = None

    def __init__(self):
        """
        对象初始化方法
        添加你需要使用的model
        格式 项目model文件夹下的文件名或者 包名1.包名2.文件名 (无.py后缀)
        """
        self.model = self.import_model('user.admin.model')

    @tornado.gen.coroutine
    def create(self, params={}):
        if self.common_utils.is_empty(['account', 'verify_code', 'password', 'check_password',
                                       'shop_id', 'admin_power'], params):
            # 必要参数非空
            raise self._gre('PARAMS_NOT_EXIST')
        # 确认密码和密码不匹配
        if cmp(params['password'], params['check_password']) != 0:
            raise self._gre('PASSWORD_NOT_MATCH')

        code = self.redis.get(self.cache_key_predix.VERIFY_CODE + params['account'])
        if params['verify_code'].lower() != code:
            raise self._gre('THIRD_PART_VERIFY_CODE_FAILED')
        else:
            self.redis.delete(self.cache_key_predix.VERIFY_CODE + params['account'])

        # 账号是否以注册
        admin_nums = yield self.do_service('user.auth.register.service', 'query_user_account_one', params)
        if admin_nums:
            params['admin_id'] = admin_nums['admin_id']
            shop_admin = yield self.model.query_admin_all(params)
            if shop_admin:
                raise self._gre('DATA_EXIST')
            res = yield self.model.create_exist_admin(params)
        else:
            salt = self.salt()
            password = self.md5(self.md5(params['password']) + salt)
            params['password'] = password
            params['salt'] = salt
            res = yield self.model.create_admin(params)

        if res is None:
            raise self._gre('SQL_EXECUTE_ERROR')
        else:
            raise self._gre('SUCCESS')

    @tornado.gen.coroutine
    def update_power(self, params={}):
        if self.common_utils.is_empty(['account', 'shop_id', 'admin_power'], params):
            # 必要参数非空
            raise self._gre('PARAMS_NOT_EXIST')
        # 根据账号查询admin_id
        data = yield self.do_service('user.auth.register.service', 'query_user_account_one', params)
        if not data:
            raise self._gre('DATA_NOT_EXIST')

        params['admin_id'] = data['admin_id']
        result = yield self.model.update_power(params)

        if result is None:
            raise self._gre('SQL_EXECUTE_ERROR')
        else:
            raise self._gr(result)

    @tornado.gen.coroutine
    def query_admin_all(self, params={}):
        if self.common_utils.is_empty(['shop_id'], params):
            # 必要参数非空
            raise self._gre('PARAMS_NOT_EXIST')
        result = yield self.model.query_admin_all(params)
        if result:
            raise self._gr(result)
        else:
            raise self._gre('SQL_EXECUTE_ERROR')

    @tornado.gen.coroutine
    def delete_admin(self, params):
        """
        删除管理员
        :param params: 
        :return: 
        """
        if self.common_utils.is_empty(['account', 'shop_id'], params):
            raise self._gre('PARAMS_NOT_EXIST')

        # 账号是否存在
        admin_nums = yield self.do_service('user.auth.register.service', 'query_user_account_one', params)
        if admin_nums:
            params['admin_id'] = admin_nums['admin_id']
        else:
            raise self._gre('DATA_NOT_EXIST')
        result = yield self.model.delete_admin(params)
        if result:
            raise self._gre('SUCCESS')
        else:
            raise self._gre('SQL_EXECUTE_ERROR')