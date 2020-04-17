# -*- coding:utf-8 -*-

"""
@author: delu
@file: common_util.py
@time: 17/4/24 上午11:31
"""
import json
import cgi
import time
import hashlib
import random
import traceback
import re
from html.parser import HTMLParser
from source.properties import Properties
from tools.logs import Logs

properties = Properties()
logger = Logs().logger


class CommonUtil(object):

    @staticmethod
    def get_loader_version(path=None):
        """
        获取调用者的Version
        """
        version = None
        if path:
            version = re.findall(r"^v(.+?)\.", path)
            if version:
                version = 'v' + version[0]

        if not version:
            caller = traceback.extract_stack()[-3]
            caller_path = caller[0]
            version = re.findall(r"/src/module/(.+?)/", caller_path)
            if version:
                version = version[0]
        return version
