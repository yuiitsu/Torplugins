# -*- coding:utf-8 -*-
"""
同步数据类
"""

# import MySQLdb
import pymysql
from DBUtils.PooledDB import PooledDB
from source.properties import Properties
from source.sql_builder import SqlBuilder
from source.sql_constants import SqlConstants
from source.sql_builder_orm import SqlBuilderOrm
from tools.logs import Logs

properties = Properties()


class ModelBase(SqlBuilder):
    """
    数据类
    """
    sql_constants = SqlConstants
    pool = PooledDB(
        creator=pymysql,
        mincached=1,
        maxcached=5,
        blocking=True,
        reset=True,
        host=properties.get('jdbc', 'DB_HOST'),
        user=properties.get('jdbc', 'DB_USER'),
        passwd=properties.get('jdbc', 'DB_PASS'),
        db=properties.get('jdbc', 'DB_BASE'),
        port=int(properties.get('jdbc', 'DB_PORT')),
        use_unicode=1,
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )
    sql_builder_orm = None
    if not sql_builder_orm:
        sql_builder_orm = SqlBuilderOrm()

    logger = Logs().logger

    def __init__(self):
        """
        初始化
        """
        self.conn = self.pool.connection()
        self.cursor = self.conn.cursor()

    def get_conn(self):
        conn = self.pool.connection()
        return conn.cursor()

    def do_sqls(self, params_list):
        # 执行多条sql
        sql = ''

        try:
            for params in params_list:
                sql_type = params[self.sql_constants.SQL_TYPE]
                table_name = params[self.sql_constants.TABLE_NAME]
                dict_data = params[self.sql_constants.DICT_DATA]
                value_tuple = params[self.sql_constants.VALUE_TUPLE]

                if sql_type == self.sql_constants.INSERT:
                    #  创建
                    sql = self.build_insert(table_name, dict_data)
                elif sql_type == self.sql_constants.BATCH_INSERT:
                    # 批量创建
                    sql = self.build_batch_insert(table_name, dict_data)
                elif sql_type == self.sql_constants.UPDATE:
                    # 更新
                    sql = self.build_update(table_name, dict_data)
                elif sql_type == self.sql_constants.DELETE:
                    # 删除
                    sql = self.build_delete(table_name, dict_data)
                self.logger.info('sql:{}, value: {}'.format(sql, value_tuple))
                self.cursor.execute(sql, value_tuple)
            if params_list:
                self.conn.commit()
                return self.sql_constants.SUCCESS
        except Exception as e:
            self.conn.rollback()
            self.logger.exception(e)
            return None

    def page_find(self, table_name, params, value_tuple, auto_commit=True):
        """
        分页查询
        :param params: 
        :return: 
        """
        # 分页查询
        sql = self.build_paginate(table_name, params)
        sql_count = self.build_get_rows(table_name, params)
        try:
            self.cursor.execute(sql, value_tuple)
            dict_list = self.cursor.fetchall()

            self.cursor.execute(sql_count, value_tuple)
            dic_rows = self.cursor.fetchone()

            return [dict_list, dic_rows[self.sql_constants.ROW_COUNT] if dic_rows else 0]
        except Exception as e:
            self.logger.exception(e)
            return None

    def get_rows(self, table_name, params, value_tuple, auto_commit=True):
        """
        统计数量
        :param params: 
        :return: 
        """
        sql_count = self.build_get_rows(table_name, params)
        try:
            self.cursor.execute(sql_count, value_tuple)
            dic_rows = self.cursor.fetchone()

            return dic_rows[self.sql_constants.ROW_COUNT] if dic_rows else 0
        except Exception as e:
            self.logger.exception(e)
            return 0

    def find(self, table_name, params={}, value_tuple=(), str_type='one', auto_commit=True):
        """
        查询
        :param params: 
        :return: 
        """
        sql = self.build_select(table_name, params)
        try:

            self.cursor.execute(sql, value_tuple)
            if str_type == self.sql_constants.LIST:
                return self.cursor.fetchall()
            else:
                return self.cursor.fetchone()
        except Exception as e:
            self.logger.exception(e)
            return False

    def insert(self, table_name, params, value_tuple, auto_commit=True):
        """
        创建
        :param params: 
        :return: 
        """
        sql = self.build_insert(table_name, params)
        try:
            self.cursor.execute(sql, value_tuple)
            if auto_commit:
                self.conn.commit()
            id = self.cursor.lastrowid
            result = self.sql_constants.SUCCESS.copy()
            result['last_id'] = id
            return result
        except Exception as e:
            self.logger.exception(e)
            return None

    def batch_insert(self, table_name, params, value_tuple, auto_commit=True):
        """
        批量插入
        :param table_name: 
        :param params: 
        :param value_tuple: 
        :param auto_commit: 
        :return: 
        """
        sql = self.build_batch_insert(table_name, params)
        try:
            self.cursor.execute(sql, value_tuple)
            if auto_commit:
                self.conn.commit()
            return self.sql_constants.SUCCESS
        except Exception as e:
            self.logger.exception(e)
            return None

    def update(self, table_name, params, value_tuple, auto_commit=True):
        """
        更新
        :param params: 
        :return: 
        """
        sql = self.build_update(table_name, params)
        self.logger.info('sql:{}, value: {}'.format(sql, value_tuple))
        try:
            self.cursor.execute(sql, value_tuple)
            if auto_commit:
                self.conn.commit()
            return self.sql_constants.SUCCESS
        except Exception as e:
            self.logger.exception(e)
            return None

    def delete(self, table_name, params, value_tuple, auto_commit=True):
        """
        删除
        :param params: 
        :return: 
        """
        sql = self.build_delete(table_name, params)
        try:
            self.cursor.execute(sql, value_tuple)
            if auto_commit:
                self.conn.commit()
            return self.sql_constants.SUCCESS
        except Exception as e:
            self.logger.exception(e)
            return None

    def do_sqls_orm(self, params_list):
        # 执行多条sql
        sql = ''
        try:
            for params in params_list:
                sql_type = params[self.sql_constants.SQL_TYPE]
                table_name = params[self.sql_constants.TABLE_NAME]
                dict_data = params[self.sql_constants.DICT_DATA]
                value_params = params[self.sql_constants.VALUE_PARAMS]

                if sql_type == self.sql_constants.INSERT:
                    #  创建
                    sql, value_tuple = self.sql_builder_orm.build_insert(table_name, dict_data, value_params)
                elif sql_type == self.sql_constants.UPDATE:
                    # 更新
                    sql, value_tuple = self.sql_builder_orm.build_update(table_name, dict_data, value_params)
                elif sql_type == self.sql_constants.DELETE:
                    # 删除
                    sql, value_tuple = self.sql_builder_orm.build_delete(table_name, dict_data, value_params)
                self.cursor.execute(sql, value_tuple)
            if params_list:
                self.conn.commit()
                return self.sql_constants.SUCCESS
        except Exception as e:
            self.conn.rollback()
            self.logger.exception(e)
            return None

    def page_find_orm(self, table_name, dict_data, params):
        """
        分页查询
        :param params: 
        :return: 
        """
        # 分页查询
        sql, value_tuple = self.sql_builder_orm.build_paginate(table_name, dict_data, params)
        sql_count, count_value_tuple = self.sql_builder_orm.build_count(table_name, dict_data, params)
        try:
            self.cursor.execute(sql, value_tuple)
            dict_list = self.cursor.fetchall()

            self.cursor.execute(sql_count, count_value_tuple)
            dic_rows = self.cursor.fetchone()
            data = {
                'list': dict_list,
                'row_count': dic_rows[self.sql_constants.ROW_COUNT] if dic_rows else 0
            }
            return data
        except Exception as e:
            self.logger.exception(e)
            return None

    def get_rows_orm(self, table_name, dict_data, params):
        """
        统计数量
        :param params: 
        :return: 
        """
        sql_count, value_tuple = self.sql_builder_orm.build_count(table_name, dict_data, params)
        try:
            self.cursor.execute(sql_count, value_tuple)
            dic_rows = self.cursor.fetchone()

            return dic_rows[self.sql_constants.ROW_COUNT] if dic_rows else 0
        except Exception as e:
            self.logger.exception(e)
            return 0

    def find_orm(self, table_name, dict_data, params={}, str_type='one'):
        """
        查询
        :param params: 
        :return: 
        """
        sql, value_tuple = self.sql_builder_orm.build_select(table_name, dict_data, params)
        try:

            self.cursor.execute(sql, value_tuple)
            if str_type == self.sql_constants.LIST:
                return self.cursor.fetchall()
            else:
                return self.cursor.fetchone()
        except Exception as e:
            self.logger.exception(e)
            return False

    def insert_orm(self, table_name, dict_data, params, auto_commit=True):
        """
        创建
        :param params: 
        :return: 
        """
        sql, value_tuple = self.sql_builder_orm.build_insert(table_name, dict_data, params)
        try:
            self.cursor.execute(sql, value_tuple)
            if auto_commit:
                self.conn.commit()
            id = self.cursor.lastrowid
            result = self.sql_constants.SUCCESS.copy()
            result['last_id'] = id
            return result
        except Exception as e:
            self.logger.exception(e)
            return None

    def update_orm(self, table_name, dict_data, params, auto_commit=True):
        """
        更新
        :param params: 
        :return: 
        """
        sql, value_tuple = self.sql_builder_orm.build_update(table_name, dict_data, params)
        try:
            self.cursor.execute(sql, value_tuple)
            if auto_commit:
                self.conn.commit()
            return self.sql_constants.SUCCESS
        except Exception as e:
            self.logger.exception(e)
            return None

    def delete_orm(self, table_name, dict_data, params, auto_commit=True):
        """
        删除
        :param params: 
        :return: 
        """
        sql, value_tuple = self.sql_builder_orm.build_delete(table_name, dict_data, params)
        try:
            self.cursor.execute(sql, value_tuple)
            if auto_commit:
                self.conn.commit()
            return self.sql_constants.SUCCESS
        except Exception as e:
            self.logger.exception(e)
            return None

    def __del__(self):
        pass
        # self.cursor.close()
        # self.conn.close()
        # self.db.close()
