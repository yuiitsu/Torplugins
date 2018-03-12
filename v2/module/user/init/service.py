# -*- coding:utf-8 -*-

"""
@author zzx
@time 2017/7/4
"""
import tornado.gen
from base.service import ServiceBase


class Service(ServiceBase):

    @tornado.gen.coroutine
    def init_dm(self, params):
        """
        初始化theme
        :param params:
        :return:
        """
        if self.common_utils.is_empty(['shop_id', 'admin_id'], params):
            raise self._gre('PARAMS_NOT_EXIST')

        # 检查店铺是否已经存在模板，如果不存在，执行店铺模板数据初始化
        theme_list_result = yield self.do_service('dm.theme.service', 'query_shop_theme_list', params)
        if theme_list_result and theme_list_result['code'] == 0 and len(theme_list_result['data']) > 0:
            raise self._gre('DATA_EXIST')

        # 执行店铺模板数据初始化
        default_theme_result = yield self.do_service('cfg.dm.theme.service', 'query_theme_default', params)
        if default_theme_result and default_theme_result['code'] == 0:
            default_theme_data = theme_list_result['data']
            default_theme_data['shop_id'] = params['shop_id']
            default_theme_data['admin_id'] = params['admin_id']

            init_shop_default_theme_result = yield self.do_service('dm.theme.service',
                                                                   'init_shop_default_theme', params)
            if init_shop_default_theme_result:
                raise self._gre('DM_INIT_FAILED')

            raise self._gre('DATA_EXIST')
        else:
            # 查询失败
            raise self._gre('CFG_THEME_NOT_FIND')

