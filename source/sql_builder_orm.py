# -*- coding:utf-8 -*-

"""
@author: delu
@file: sql_builder.py
@time: 17/4/20 上午10:23
"""
from source.base_sql_builder import BaseSqlBuilder


class SqlBuilderOrm(BaseSqlBuilder):
    def build_select(self, table_name, dict_data, params):
        """ 
        读取一组数据
        @params str_table_name string 表名
        @params str_type string 类型，可以是list, first
        @prams dic_data dict 数据字典
        @params booformat_data bool 是否格式化数据，默认为True
        """
        value_list = []
        fields = self.build_fields(dict_data)
        join = self.build_join(dict_data)
        condition = self.build_condition(dict_data, params, value_list)
        group_by = self.build_group_by(dict_data)
        having = self.build_having(dict_data)
        order = self.build_order(dict_data)
        limit = self.build_limit(dict_data)

        str_sql = "select %s from %s %s %s %s %s %s %s" % (
        fields, table_name, join, condition, group_by, having, order, limit)
        return str_sql, tuple(value_list)

    def build_insert(self, table_name, dict_data, params):
        """
        构建insert
        :param table_name: 
        :param dict_data: 
        :param params: 
        :return: 
        """
        value_list = []

        key = self.build_key(dict_data, params, value_list)
        val = self.build_val(dict_data)
        duplicate_key = self.build_duplicate_key(dict_data, params, value_list)

        str_sql = ' insert into %s (%s) values(%s) %s ' % (table_name, key, val, duplicate_key)
        return str_sql, tuple(value_list)

    def build_update(self, table_name, dict_data, params):
        """
        构建update
        :param table_name: 
        :param dict_data: 
        :param params: 
        :return: 
        """
        value_list = []
        update_fields = self.build_update_fields(dict_data, params, value_list)
        condition = self.build_condition(dict_data, params, value_list)
        str_sql = ' update %s set %s %s ' % (table_name, update_fields, condition)
        return str_sql, tuple(value_list)

    def build_delete(self, table_name, dict_data, params):
        """
        构建delete
        :param table_name: 
        :param dict_data: 
        :param params: 
        :return: 
        """
        value_list = []

        condition = self.build_condition(dict_data, params, value_list)
        str_sql = ' delete from %s %s ' % (table_name, condition)
        return str_sql, tuple(value_list)

    def build_count(self, table_name, dict_data, params):
        """
        构建统计
        :param table_name: 
        :param dict_data: 
        :param params: 
        :return: 
        """
        value_list = []
        join = self.build_join(dict_data)
        condition = self.build_condition(dict_data, params, value_list)
        str_sql = ' select count(*) as row_count from %s %s %s ' % (table_name, join, condition)
        return str_sql, tuple(value_list)

    def build_paginate(self, table_name, dict_data, params):
        """
        构建分页查询语句
        :param table_name: 
        :param dict_data: 
        :param params: 
        :return: 
        """
        if 'page_index' not in params or 'page_size' not in params:
            params['page_index'] = 1
            params['page_size'] = 10
        dict_data[self.sql_constants.LIMIT] = [params['page_index'], params['page_size']]
        return self.build_select(table_name, dict_data, params)
