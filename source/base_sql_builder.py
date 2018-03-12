# -*- coding:utf-8 -*-

"""
@author: delu
@file: base_sql_builder.py
@time: 17/7/3 23:11
"""
from source.sql_constants import SqlConstants


class BaseSqlBuilder(object):
    sql_constants = SqlConstants

    def build_fields(self, dict_data):
        """
        构建fields
        :param dict_data: 
        :return: 
        """
        fields = ''
        if self.sql_constants.FIELDS in dict_data and dict_data[self.sql_constants.FIELDS]:
            if isinstance(dict_data[self.sql_constants.FIELDS], list):
                fields += ','.join(dict_data[self.sql_constants.FIELDS])
            else:
                fields += dict_data[self.sql_constants.FIELDS]
        else:
            fields += ' * '
        return fields

    def build_join(self, dict_data):
        """
        构建join
        :param dict_data: 
        :return: 
        """
        join = ''
        if self.sql_constants.JOIN in dict_data and dict_data[self.sql_constants.JOIN]:
            for join_item in dict_data[self.sql_constants.JOIN]:
                join += ' left join %s on ( %s ) ' % (
                    join_item[self.sql_constants.TABLE_NAME], join_item[self.sql_constants.JOIN_CONDITION])
        return join

    def build_condition(self, dict_data, params, value_list):
        """ 构建条件

        @params dicCondition dict 条件字典
        """
        str_condition = ''
        if self.sql_constants.CONDITION in dict_data and dict_data[self.sql_constants.CONDITION]:
            dict_condition = dict_data[self.sql_constants.CONDITION]
            if dict_condition:
                if isinstance(dict_condition, list):
                    list_condition = []
                    for condition_key in dict_condition:
                        if condition_key in params and params[condition_key]:
                            list_condition.append(' ' + condition_key + '=%s ')
                            value_list.append(params[condition_key])
                    str_condition += 'and'.join(list_condition)
                elif isinstance(dict_condition, dict):
                    temp_str_condition_list = []
                    for key, val in dict_condition.iteritems():
                        temp_str_condition = ' ('
                        if isinstance(val, list):
                            val_list = []
                            for val_item in val:
                                if val_item in params and params[val_item]:
                                    val_list.append(' ' + val_item + '=%s ')
                                    value_list.append(params[val_item])
                            temp_str_condition += key.join(val_list)
                        elif isinstance(val, dict):
                            inner_val_list = []
                            for inner_key, inner_val in val.iteritems():
                                if isinstance(inner_val, list):
                                    for inner_key_item in inner_val:
                                        if cmp(inner_key.lower(), self.sql_constants.IN) == 0:
                                            # 处理in关键字
                                            temp_key = inner_key_item + '_list'
                                            if temp_key in params and params[temp_key]:
                                                inner_val_list.append(
                                                    ' ' + inner_key_item + ' ' + self.build_in(len(params[temp_key])))
                                                value_list.extend(params[temp_key])
                                        elif inner_key_item in params and params[inner_key_item]:
                                            inner_val_list.append(' ' + inner_key_item + ' ' + inner_key + ' ' + '%s ')
                                            if cmp(inner_key_item.lower(), self.sql_constants.LIKE) == 0:
                                                value_list.append('\'%' + params[inner_key_item] + '%\'')
                                            else:
                                                value_list.append(params[inner_key_item])
                            temp_str_condition += key.join(inner_val_list)
                        temp_str_condition += ') '
                        temp_str_condition_list.append(temp_str_condition)
                    str_condition += 'and'.join(temp_str_condition_list)
        return 'where %s' % str_condition if str_condition else ''

    def build_group_by(self, dict_data):
        """
        构建group_by
        :param dict_data: 
        :return: 
        """
        group_by = ''
        if self.sql_constants.GROUP_BY in dict_data and dict_data[self.sql_constants.GROUP_BY]:
            group_by += ' group by %s ' % dict_data[self.sql_constants.GROUP_BY]
        return group_by

    def build_having(self, dict_data):
        """
        构建having
        :param dict_data: 
        :return: 
        """
        having = ''
        if self.sql_constants.HAVING in dict_data and dict_data[self.sql_constants.HAVING]:
            having += ' having %s ' % dict_data[self.sql_constants.HAVING]
        return having

    def build_order(self, dict_data):
        """
        构建order
        :param dict_data: 
        :return: 
        """
        order = ''
        if self.sql_constants.ORDER in dict_data and dict_data[self.sql_constants.ORDER]:
            order += ' order by %s ' % dict_data[self.sql_constants.ORDER]
        return order

    def build_limit(self, dict_data):
        """
        构建limit
        :param dict_data: 
        :return: 
        """
        limit = ''
        if self.sql_constants.LIMIT in dict_data and dict_data[self.sql_constants.LIMIT]:
            page_index = int(dict_data[self.sql_constants.LIMIT][0])
            page_size = int(dict_data[self.sql_constants.LIMIT][1])
            limit += ' limit %s, %s ' % (str(int(page_index - 1) * int(page_size)), str(page_size))
        return limit

    def build_key(self, dict_data, params, value_list):
        """
        构建key
        :param dict_data: 
        :param value_list: 
        :param params: 
        :return: 
        """
        key = ''
        if self.sql_constants.KEY in dict_data and dict_data[self.sql_constants.KEY]:
            if isinstance(dict_data[self.sql_constants.KEY], str):
                dict_data[self.sql_constants.KEY] = dict_data[self.sql_constants.KEY].spilt(',')
            if isinstance(dict_data[self.sql_constants.KEY], list):
                key += ','.join(dict_data[self.sql_constants.KEY])
                for key_item in dict_data[self.sql_constants.KEY]:
                    value_list.append(params[key_item])
        return key

    def build_val(self, dict_data):
        """
        构建val
        :param dict_data: 
        :return: 
        """
        val = ''
        if self.sql_constants.KEY in dict_data and dict_data[self.sql_constants.KEY]:
            if isinstance(dict_data[self.sql_constants.KEY], list):
                val_list = []
                for key in dict_data[self.sql_constants.KEY]:
                    val_list.append('%s')
                val += ','.join(val_list)
        return val

    def build_duplicate_key(self, dict_data, params, value_list):
        """
        主键重复，则更新
        :param dict_data: 
        :param params: 
        :param value_list: 
        :return: 
        """
        duplicate_key = ''
        if self.sql_constants.DUPLICATE_KEY_UPDATE in dict_data and dict_data[self.sql_constants.DUPLICATE_KEY_UPDATE]:
            if isinstance(dict_data[self.sql_constants.DUPLICATE_KEY_UPDATE], list):
                key_list = []
                for key in dict_data[self.sql_constants.DUPLICATE_KEY_UPDATE]:
                    if key in params and params[key]:
                        key_list.append('' + key + '=%s ')
                        value_list.append(params[key])
                duplicate_key += ','.join(key_list)
        return duplicate_key

    def build_update_fields(self, dict_data, params, value_list):
        """
        构建update_fields
        :param dict_data: 
        :return: 
        """
        update_fields = ''
        if self.sql_constants.UPDATE_FIELDS in dict_data and dict_data[self.sql_constants.UPDATE_FIELDS]:
            if isinstance(dict_data[self.sql_constants.UPDATE_FIELDS], list):
                fields_list = []
                for fields in dict_data[self.sql_constants.UPDATE_FIELDS]:
                    if fields in params and params[fields]:
                        fields_list.append(' ' + fields + '=%s ')
                        value_list.append(params[fields])
                update_fields += ','.join(fields_list)
        return update_fields

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
