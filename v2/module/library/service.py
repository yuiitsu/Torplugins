# -*- coding:utf-8 -*-

"""
@author: xhb
@file: service.py
@time: 17/11/8 下午10:05
"""
import tornado.gen
from base.service import ServiceBase


class Service(ServiceBase):

    category_model = None

    def __init__(self):
        """
        对象初始化方法
        添加你需要使用的model
        格式 项目model文件夹下的文件名或者 包名1.包名2.文件名 (无.py后缀)
        """
        self.category_model = self.import_model('library.category.model')

    @tornado.gen.coroutine
    def create_category(self, params):
        """
        创建目录
        :param params:
        :return:
        """
        if self.common_utils.is_empty(['admin_id'], params):
            raise self._gre('PARAMS_NOT_EXIST')

        if not params.get('category_name') or params['category_name'] == '':
            params['category_name'] = '新建文件夹'

        result = yield self.category_model.create_category(params)
        if result is None:
            raise self._gre('SQL_EXECUTE_ERROR')
        else:
            raise self._grs(result)

    @tornado.gen.coroutine
    def update_category(self, params):
        """
        修改目录名字
        :param params:
        :return:
        """
        # 检查参数
        if self.common_utils.is_empty(['category_id', 'category_name', 'admin_id'], params):
            raise self._gre('PARAMS_NOT_EXIST')

        result = yield self.category_model.update_category(params)
        if result is None:
            raise self._gre('SQL_EXECUTE_ERROR')
        else:
            raise self._grs(result)

    @tornado.gen.coroutine
    def delete_category(self, params):
        """
        批量删除文件夹
        :param params:
        :return:
        """
        if self.common_utils.is_empty(['category_id_list', 'admin_id'], params):
            raise self._gre('PARAMS_NOT_EXIST')

        if isinstance(params['category_id_list'], str):
            params['category_id_list'] = self.json.loads(params['category_id_list'])

        # 检查文件夹里有没有资源，有的话不让删
        data_result = yield self.do_service('library.service', 'query_category_data', params=params)
        if data_result['code'] == 0 and data_result['data']:
            raise self._grs('请先删除文件夹里的资源')

        elif data_result['code'] != 0:
            raise self._gr(data_result)

        elif data_result['code'] == 0 and not data_result['data']:
            result = yield self.category_model.delete_category(params)
            if result is None:
                raise self._gre('SQL_EXECUTE_ERROR')
            else:
                raise self._grs(result)

    @tornado.gen.coroutine
    def query_category_list(self, params):
        """
        查询目录
        :param params:
        :return:
        """
        category_result = yield self.category_model.query_list(params)
        if category_result is None:
            raise self._gre('SQL_EXECUTE_ERROR')
        else:
            raise self._grs(category_result)
