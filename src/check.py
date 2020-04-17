# -*- coding: utf-8 -*-

"""
检查脚本，主要检查以下信息
1. 各配置文件
2. 数据库表/字段
@author: Yuiitsu
@file: check
@time: 2018/7/26 14:52
"""
import os
import sys


parent_path = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.dirname(parent_path)
sys.path.append(parent_path)
sys.path.append(root_path)


import configparser
from tools.logs import Logs

logger = Logs().logger


class CheckService:

    @classmethod
    def build_data(cls, target_dir, data):
        for parent, dir_names, file_names in os.walk(target_dir):
            for file_name in file_names:
                if os.path.splitext(file_name)[1] != '.conf':
                    continue

                data[file_name] = {}
                properties = configparser.ConfigParser()
                try:
                    properties.read(parent + "/" + file_name, encoding='utf-8')
                except Exception as e:
                    logger.exception(e)

                sections = properties.sections()
                for item in sections:
                    data[file_name][item] = {}
                    options = properties.options(item)
                    for option in options:
                        value = properties.get(item, option)
                        data[file_name][item][option] = value

    @classmethod
    def config_file(cls):
        """
        检查配置文件
            1. 读取参考配置文件
            2. 读取目标配置文件
            3. 对比各文件的内容
        :return:
        """
        source_dir = '../../conf/'
        target_dir = '/apps/conf/wmb2c/'

        # 1
        source_data = {}
        cls.build_data(source_dir, source_data)

        # 2
        target_data = {}
        cls.build_data(target_dir, target_data)

        # 3
        for source_file, source_sections in source_data.items():
            if source_file in target_data:
                print('\033[0;32m\t Check file [{}] pass.\033[0m'.format(source_file))
                target_sections = target_data[source_file]
                for source_section, source_options in source_sections.items():
                    if source_section in target_sections:
                        print('\033[0;32m\t Check file [{}] section [{}] pass.\033[0m'.format(source_file, source_section))
                        target_options = target_sections[source_section]
                        for source_option in source_options:
                            if source_option in target_options:
                                print('\033[0;32m\t Check file [{}] section [{}] option [{}] pass.\033[0m'.format(source_file, source_section, source_option))
                            else:
                                print('\033[0;31m\t Check file [{}] section [{}] option [{}] failed.\033[0m'.format(source_file, source_section, source_option))
                    else:
                        print('\033[0;31m\t Check file [{}] section [{}] pass.\033[0m'.format(source_file, source_section))
            else:
                print('\033[0;31m\t Check file [{}] failed.\033[0m'.format(source_file))

    @classmethod
    def start(cls):
        logger.info("""
            Check Service Start.
        """)
        cls.config_file()


if __name__ == '__main__':
    CheckService.start()
