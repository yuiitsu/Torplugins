# -*- coding:utf-8 -*-

"""
@author: delu
@file: pic_service.py
@time: 17/5/16 下午1:23
"""
from base.service import ServiceBase
import tornado.gen


class Service(ServiceBase):
    """
    pic_service
    """

    images_model = None

    def __init__(self):
        """
        对象初始化方法
        添加你需要使用的model
        格式 项目model文件夹下的文件名或者 包名1.包名2.文件名 (无.py后缀)
        """
        self.images_model = self.import_model('user.model.images.images_model')

    @tornado.gen.coroutine
    def create_image(self, params):
        """
        创建图片
        :param params: 
        :return: 
        """
        if self.common_utils.is_empty(['image_list', 'admin_id'], params):
            raise self._gre('PARAMS_NOT_EXIST')
        if isinstance(params['image_list'], str):
            params['image_list'] = self.json.loads(params['image_list'])
        result = yield self.images_model.create_image_batch(params)
        if result is None:
            raise self._gre('SQL_EXECUTE_ERROR')
        else:
            result = self._e('SUCCESS')
            result['data'] = {'host_type': self.properties.get('images', 'HOST_TYPE')}
            raise self._gr(result)

    @tornado.gen.coroutine
    def delete_image(self, params):
        """
        删除图片
        :param params: 
        :return: 
        """
        if self.common_utils.is_empty(['img_key_list', 'admin_id'], params):
            raise self._gre('PARAMS_NOT_EXIST')
        if isinstance(params['img_key_list'], str):
            params['img_key_list'] = self.json.loads(params['img_key_list'])
        result = yield self.images_model.delete_image(params)
        if result is None:
            raise self._gre('SQL_EXECUTE_ERROR')
        else:
            raise self._gre('SUCCESS')

    @tornado.gen.coroutine
    def query_image_list(self, params):
        """
        查询图片
        :param params: 
        :return: 
        """
        image_result = yield self.images_model.query_list(params)
        if image_result is None:
            raise self._gre('SQL_EXECUTE_ERROR')
        else:
            result = self._e('SUCCESS')
            result['data'] = image_result
            raise self._gr(result)
