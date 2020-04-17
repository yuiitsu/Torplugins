# -*- coding:utf-8 -*-

"""
@author: delu
@file: sql_builder.py
@time: 17/4/20 上午10:23
"""
import pymysql
from source.properties import Properties
from source.sql_constants import SqlConstants

properties = Properties()


class SqlBuilder(object):
    sql_constants = SqlConstants

    def build_select(self, str_table_name, dic_data, boo_format_data=True):
        """ 
        读取一组数据

        @params str_table_name string 表名
        @params str_type string 类型，可以是list, first
        @prams dic_data dict 数据字典
        @params booformat_data bool 是否格式化数据，默认为True
        """
        if boo_format_data:
            dic_data = self.format_data(dic_data)

        str_table_name = self.build_table_name(str_table_name)

        str_fields = self.build_fields(dic_data[SqlConstants.FIELDS])

        str_condition = self.build_condition(dic_data[SqlConstants.CONDITION])

        str_join = ''

        for join_item in dic_data[SqlConstants.JOIN]:
            str_join += self.build_join(join_item)

        str_limit = self.build_limit(dic_data[SqlConstants.LIMIT])

        str_order = self.build_order(dic_data[SqlConstants.ORDER])

        str_group_by = self.build_group_by(dic_data[SqlConstants.GROUP_BY])

        str_sql = "select %s from %s %s %s %s %s %s" % (
            str_fields, str_table_name, str_join, str_condition, str_group_by, str_order, str_limit)

        return str_sql

    def build_paginate(self, str_table_name, dic_data):
        """ 分页读取数据

        @params str_table_name string 表名
        @params dic_data dict 数据字典，可以包裹field, fields, condition等key
        """

        dic_data = self.format_data(dic_data)

        # 页码
        int_page = dic_data[SqlConstants.LIMIT][0] if SqlConstants.LIMIT in dic_data and dic_data[SqlConstants.LIMIT][
            0] else '1'
        int_page_num = dic_data[SqlConstants.LIMIT][1] if SqlConstants.LIMIT in dic_data and \
                                                          dic_data[SqlConstants.LIMIT][1] else '10'
        int_start_limit = (int(int_page) - 1) * int(int_page_num)

        dic_data[SqlConstants.LIMIT] = [str(int_start_limit), str(int_page_num)]

        # 获取数据
        return self.build_select(str_table_name, dic_data, False)

    def build_get_rows(self, str_table_name, dic_data, booformat_data=True):
        """ 获取数据记录数

        @params str_table_name string 表名
        @params dic_data dict 数据字典
        @params booformat_data bool 是否格式化数据，默认为True
        """

        if booformat_data:
            dic_data = self.format_data(dic_data)

        str_table_name = self.build_table_name(str_table_name)

        str_join = ''

        for join_item in dic_data[SqlConstants.JOIN]:
            str_join += self.build_join(join_item)

        str_condition = self.build_condition(dic_data[SqlConstants.CONDITION])

        return "select count(*) as row_count from %s %s %s" % (str_table_name, str_join, str_condition)

    def build_insert(self, str_table_name, dic_data):
        """ 插入数据

        @params str_table_name string 表名
        @params dic_data dict 数据字典
        """
        dic_data = self.format_data(dic_data)
        str_table_name = self.build_table_name(str_table_name)
        str_duplicate_key = self.build_on_duplicate_key_update(dic_data[SqlConstants.DUPLICATE_KEY_UPDATE])
        return "insert into %s (%s) values (%s) %s" % (str_table_name,
                                                       dic_data[SqlConstants.KEY],
                                                       dic_data[SqlConstants.VAL],
                                                       str_duplicate_key)

    def build_batch_insert(self, str_table_name, dic_data):
        """
        批量插入数据
        :param str_table_name: 
        :param dic_data: 
        :return: 
        """
        dic_data = self.format_data(dic_data)
        str_table_name = self.build_table_name(str_table_name)
        str_duplicate_key = self.build_on_duplicate_key_update(dic_data[SqlConstants.DUPLICATE_KEY_UPDATE])
        return "insert into %s (%s) values %s %s" % (str_table_name, dic_data[SqlConstants.KEY],
                                                     ','.join(dic_data[SqlConstants.BATCH_VAL]), str_duplicate_key)

    def build_update(self, str_table_name, dic_data):
        """ 修改数据

        @params str_table_name string 表名
        @params dic_data dict 数据字典
        """

        dic_data = self.format_data(dic_data)
        str_table_name = self.build_table_name(str_table_name)
        str_fields = self.build_fields(dic_data[SqlConstants.FIELDS])
        str_condition = self.build_condition(dic_data[SqlConstants.CONDITION])

        return "update %s set %s %s" % (str_table_name, str_fields, str_condition)

    def build_delete(self, str_table_name, dic_data):
        """ 删除数据

        @params str_table_name string 表名
        @params dic_data dict 数据字典
        """

        dic_data = self.format_data(dic_data)
        str_table_name = self.build_table_name(str_table_name)
        str_condition = self.build_condition(dic_data[SqlConstants.CONDITION])

        str_sql = "delete from %s %s" % (str_table_name, str_condition)
        return str_sql

    def format_data(self, dic_data):
        """ 格式化数据
        将fields, condition, join 等数据格式化返回

        @params dic_data dict 数据字典
        """

        # fileds
        dic_data[SqlConstants.FIELDS] = dic_data[SqlConstants.FIELDS] if SqlConstants.FIELDS in dic_data else ''

        # join
        dic_data[SqlConstants.JOIN] = dic_data[SqlConstants.JOIN] if SqlConstants.JOIN in dic_data else []

        # conditon
        dic_data[SqlConstants.CONDITION] = dic_data[
            SqlConstants.CONDITION] if SqlConstants.CONDITION in dic_data else ''

        # order
        dic_data[SqlConstants.ORDER] = dic_data[SqlConstants.ORDER] if SqlConstants.ORDER in dic_data else ''

        # group_by
        dic_data[SqlConstants.GROUP_BY] = dic_data[SqlConstants.GROUP_BY] if SqlConstants.GROUP_BY in dic_data else ''

        # having
        dic_data[SqlConstants.HAVING] = dic_data[SqlConstants.HAVING] if SqlConstants.HAVING in dic_data else ''

        # limit
        dic_data[SqlConstants.LIMIT] = dic_data[SqlConstants.LIMIT] if SqlConstants.LIMIT in dic_data else ''

        if SqlConstants.KEY in dic_data:
            if isinstance(dic_data[SqlConstants.KEY], str):
                dic_data[SqlConstants.KEY] = dic_data[SqlConstants.KEY].split(',')
            val_list = []
            for key in dic_data[SqlConstants.KEY]:
                val_list.append('%s')
            # val
            dic_data[SqlConstants.VAL] = ','.join(val_list)
            # key
            dic_data[SqlConstants.KEY] = ','.join(dic_data[SqlConstants.KEY])

        # duplicate_key_update
        dic_data[SqlConstants.DUPLICATE_KEY_UPDATE] = dic_data[
            SqlConstants.DUPLICATE_KEY_UPDATE] if SqlConstants.DUPLICATE_KEY_UPDATE in dic_data else ''

        return dic_data

    def build_table_name(self, str_table_name):
        """ 构建表名
        根据配置文件中的表前辍，构建表名

        @params str_table_name string 表名
        """

        str_table_name = properties.get('jdbc', 'DB_TABLE_PRE') + str_table_name \
            if properties.get('jdbc', 'DB_TABLE_PRE') else str_table_name

        return str_table_name

    def build_fields(self, lisFields):
        """ 构建读取字段

        @params lisFields list 字段列表
        """

        str_fields = ','.join(lisFields) if lisFields else '*'

        return str_fields

    def build_join(self, str_join):
        """ 构建Join

        @params dicCondition dict 条件字典
        """

        return 'LEFT JOIN %s ON (%s)' % (str_join[SqlConstants.TABLE_NAME] if str_join[SqlConstants.TABLE_NAME] else '',
                                         str_join[SqlConstants.JOIN_CONDITION] if str_join[
                                             SqlConstants.JOIN_CONDITION] else '')

    def build_condition(self, str_condition):
        """ 构建条件

        @params dicCondition dict 条件字典
        """

        return 'where %s' % str_condition if str_condition else ''

    def build_group_by(self, str_group_by):
        """
        分组条件
        :param str_group_by: 
        :return: 
        """
        return 'group by %s' % str_group_by if str_group_by else ''

    def build_having(self, str_having):
        """
        分组过滤条件
        :param str_having:
        :return:
        """
        return 'having %s' % str_having if str_having else ''

    def build_order(self, str_order):
        """ 构建order
        未完成

        @params
        """

        # str_order = str_order

        return 'order by ' + str_order if str_order else ''

    def build_limit(self, lisLimit):
        """ 构建limit

        @params lisLimit list limit
        """

        str_limit = ','.join(lisLimit) if lisLimit else ''

        return 'limit ' + str_limit if str_limit else ''

    def build_on_duplicate_key_update(self, duplicate_key_list):
        """
        构建 on duplicate key update
        :param str_duplicate_key: 
        :return: 
        """
        if duplicate_key_list:
            return 'on duplicate key update ' + ','.join(duplicate_key_list)
        else:
            return ''

    # def escapeString(self, dic_data):
    #     if dic_data:
    #         if isinstance(dic_data, dict) == False:
    #             # print dic_data
    #             if type(dic_data) == str:
    #                 dic_data = dic_data.encode('utf8')
    #             return MySQLdb.escape_string(dic_data)
    #         else:
    #             for k, v in dic_data.iteritems():
    #                 # print type(v)
    #                 if type(v) == str:
    #                     v = v.encode('utf8')
    #                 # print v

    #                 dic_data[k] = MySQLdb.escape_string(str(v))
    #                 # dic_data[k] = str(v).replace('\'', '\\\'').replace('"', '\"')
    #             # exit()
    #             return dic_data
    #    return False

    def build_in(self, length=0):
        """
        构建in语句
        :param len: 
        :return: 
        """
        if not length:
            return ''
        in_sql = []
        count = 0
        while count < length:
            in_sql.append('%s')
            count = count + 1
        return ' in (' + ','.join(in_sql) + ') '

if __name__ == '__main__':
    obj = SqlBuilder()

    # condition = {
    #     'and': {
    #         'like': ['id', 'name', 'city'],
    #         '=': ['id', 'name', 'city'],
    #         '!=': ['id', 'name', 'city']
    #     },
    #     'or': {
    #         'like': ['id', 'name', 'city'],
    #         '=': ['id', 'name', 'city'],
    #         '!=': ['id', 'name', 'city']
    #     }
    # }
    # condition = ['id', 'name', 'city']
    # condition = {
    #     'and': ['id', 'name', 'city'],
    #     'or': {
    #         'like': ['id', 'name', 'city']
    #     }
    # }
    # params = {
    #     'id': 1,
    #     'name': 'hello'
    # }
    # sql = obj.build_condition_orm(condition, params)
    # print sql
    my_list = [1, 2, 3]

    my_list.extend(my_list)
