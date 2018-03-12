# -*- coding:utf-8 -*-

"""
@author: delu
@file: sql_constants.py
@time: 17/4/20 上午10:35
"""


class SqlConstants(object):

    SELECT = 'select'
    PAGE_SELECT = 'page_select'
    INSERT = 'insert'
    BATCH_INSERT = 'batch_insert'
    UPDATE = 'update'
    DELETE = 'delete'

    SQL_TYPE = 'sql_type'
    STR_TYPE = 'str_type'
    DICT_DATA = 'dict_data'
    VALUE_TUPLE = 'value_tuple'
    TABLE_NAME = 'table_name'
    VALUE_PARAMS = 'value_params'

    ONE = 'one'
    LIST = 'list'
    ROW_COUNT = 'row_count'
    PAGE = 'page'

    FIELDS = 'fields'
    UPDATE_FIELDS = 'update_fields'
    CONDITION = 'condition'
    JOIN = 'join'
    LIMIT = 'limit'
    ORDER = 'order'
    GROUP_BY = 'group_by'
    KEY = 'key'
    VAL = 'val'
    BATCH_VAL = 'batch_val'
    JOIN_CONDITION = 'join_condition'
    DUPLICATE_KEY_UPDATE = 'duplicate_key_update'

    LIKE = 'like'
    IN = 'in'
    HAVING = 'having'

    SUCCESS = {'code': 0, 'msg': '成功'}
