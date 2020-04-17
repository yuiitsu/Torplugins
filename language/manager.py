# -*- coding:utf-8 -*-

"""
@author: yuiitsu
@file: manager.py
@time: 2018/10/10 2:06 PM
"""
import importlib
from source.properties import Properties


class LangManager:

    properties = Properties()
    lang_dict = {}

    def __init__(self):
        # 配置使用的语言
        lang = self.properties.get('language', 'lang')
        lang = lang if lang else 'cn'
        # load
        model = importlib.import_module('language.' + lang)
        self.lang_dict = model.LangDict

    def get(self, key):
        """
        :param key:
        :return:
        """
        return self.lang_dict[key] if key in self.lang_dict else ''


if __name__ == "__main__":
    lang_manager = LangManager()
    lang_text = lang_manager.get('name')
    print(lang_text)
