# -*- coding:utf-8 -*-
"""
配置文件属性
"""

import ConfigParser
from tools.logs import Logs


class Properties(object):

    properties = None
    logger = Logs().logger

    def __init__(self, file_name=None):
        file_name = file_name if file_name else 'setting'
        self.properties = ConfigParser.ConfigParser()
        try:
            self.properties.read('/opt/wmb2c/' + file_name + '.conf')
        except Exception as e:
            self.logger.exception(e)

    def get(self, section, option):
        try:
            return self.properties.get(section, option)
        except Exception as e:
            self.logger.exception(e)
