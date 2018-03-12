# -*- coding:utf-8 -*-

"""
@author: delu
@file: common_util.py
@time: 17/4/24 上午11:31
"""
import json
import HTMLParser
import cgi
from source.properties import Properties
from tools.logs import Logs

properties = Properties()
logger = Logs().logger


class CommonUtil(object):

    @staticmethod
    def return_val(data, default_val=None):
        """
        有值返回，无值返回空字符串
        :param data:
        :param default_val:
        :return:
        """
        if data or data == 0:
            return data
        else:
            return '' if default_val is None else default_val

    @staticmethod
    def get_val(dict_params, key, default=''):
        """
        从字典中获取数据，如果key不存在，返回空字符串
        :param dict_params: 字典
        :param key: key
        :param default: default
        :return:
        """
        if key in dict_params:
            return dict_params[key]
        else:
            return default if default != '' else ''

    @staticmethod
    def remove_element(my_dict, element_list):
        """
        移除字典中的元素
        :param my_dict: 
        :param element_list: 
        :return: 
        """
        for element in element_list:

            if element in my_dict:
                my_dict.pop(element)
        return my_dict

    @staticmethod
    def is_empty(key_list, my_dict):
        """
        判断key_list中的元素是否存在为空的情况
        :param key_list: 
        :param my_dict: 
        :return: 
        """
        for key in key_list:
            if key not in my_dict or not my_dict[key]:
                return True
        return False

    @staticmethod
    def get_images(images):
        """
        将图片json转换成图片地址
        :param images: 
        :return: 
        """
        try:
            result = []
            image_list = json.loads(images)
        except Exception as e:
            logger.exception(e)
            return []

        try:
            for image in image_list:
                result.append(properties.get('images', 'HOST_TYPE_' + str(image['type'])) + image['key'])
            return result
        except Exception as e:
            logger.exception(e)
            return image_list

    @staticmethod
    def escape_html(content):
        """
        将HTML转义
        :param content:
        :return:
        """
        return cgi.escape(content)

    @staticmethod
    def un_escape_html(content):
        """
        反转HTML
        :param content:
        :return:
        """
        html_parser = HTMLParser.HTMLParser()
        return html_parser.unescape(content)


if __name__ == '__main__':
    common = CommonUtil()
    string = common.escape_html("<script></script>")
    print string
