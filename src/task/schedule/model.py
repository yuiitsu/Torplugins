# -*- coding:utf-8 -*-

"""
@author: delu
@file: model.py
@time: 18/6/20 17:49
"""

from source.async_model import AsyncModelBase
import tornado.gen


class Model(AsyncModelBase):
    @tornado.gen.coroutine
    def save_job(self, params):
        """
        保存定时任务
        :param params:
            param['job_id']     任务id
            param['group_name'] 任务组名
            param['start_time'] 任务开始时间
            param['repeat_count']   重复次数
            param['cron']       cron表达式
            param['path']       service路径
            param['method']     方法
            param['params']     参数
        :return: 
        """
        key = 'job_id, group_name, start_time, repeat_count, cron, path, method, params'
        value_tuple = (
            params['job_id'],
            params.get('group_name', 'default'),
            params['start_time'],
            params.get('repeat_count', 0),
            params.get('cron', ''),
            params['path'],
            params['method'],
            self.json.dumps(params['params'], cls=self.date_encoder)
        )
        result = yield self.insert('tbl_cfg_schedule_job',
                                   {
                                       self.sql_constants.KEY: key
                                   },
                                   value_tuple)
        raise self._gr(result)

    @tornado.gen.coroutine
    def update_job(self, params):
        """
        更新任务
        :param params: 
            param['job_id']     任务id
            param['group_name'] 任务组名
            param['start_time'] 任务开始时间
            param['repeat_count']   重复次数
            param['cron']       cron表达式
            param['path']       service路径
            param['method']     方法
            param['params']     参数
        :return: 
        """
        fields = [
            'start_time = %s'
        ]
        condition = ' job_id = %s '
        value_tuple = (params['start_time'], params['job_id'])
        result = yield self.update('tbl_cfg_schedule_job',
                                   {
                                       self.sql_constants.FIELDS: fields,
                                       self.sql_constants.CONDITION: condition
                                   },
                                   value_tuple)
        raise self._gr(result)

    @tornado.gen.coroutine
    def query_job_page(self, params):
        """
        分页查询定时任务
        :param params: 
                param['job_id']     任务id
                param['path']       service路径
                param['method']     方法名
                param['page_index'] 分页下标
                param['page_size']  分页大小
        :return: 
        """
        condition = ' 1=1 '
        value_list = []

        if 'job_id' in params and params['job_id']:
            condition += ' and job_id = %s '
            value_list.append(params['job_id'])
        if 'path' in params and params['path']:
            condition += ' and path = %s '
            value_list.append(params['path'])
        if 'method' in params and params['method']:
            condition += ' and method = %s '
            value_list.append(params['method'])
        if 'page_index' not in params or not params['page_index']:
            params['page_index'] = 1
            params['page_size'] = 10
        limit = [params['page_index'], params['page_size']]
        result = yield self.page_find('tbl_cfg_schedule_job',
                                      {
                                          self.sql_constants.CONDITION: condition,
                                          self.sql_constants.LIMIT: limit
                                      },
                                      tuple(value_list))
        raise self._gr(result)

    @tornado.gen.coroutine
    def query_job_one(self, params):
        """
        查询单个定时任务
        :param params: 
        :return: 
        """
        condition = ' job_id = %s '
        value_tuple = (params['job_id'],)
        result = yield self.find('tbl_cfg_schedule_job', {self.sql_constants.CONDITION: condition}, value_tuple)
        raise self._gr(result)

    @tornado.gen.coroutine
    def delete_job(self, params):
        """
        删除定时任务
        :param params: 
                param['job_id'] 必传
        :return: 
        """
        condition = ' job_id = %s '
        value_tuple = (params['job_id'],)
        result = yield self.delete('tbl_cfg_schedule_job', {self.sql_constants.CONDITION: condition}, value_tuple)
        raise self._gr(result)
