# -*- coding:utf-8 -*-

import hashlib
import json
import random
import time
import datetime
import importlib
import tornado.escape

import conf.config as config

class baseService(object):
    
    dicConfig = config.CONF

    time = time

    datetime = datetime

    json = json

    hashlib = hashlib

    def __init__(self, model):
        
        self.model = model

    def md5(self, strText):
        """ MD5加密

        @params strText string 需加密字符串
        @return strResult string 加密后字符串
        """
        strResult = hashlib.md5(strText)
        return strResult.hexdigest()


    def importModel(self, strModelName, strModelDir = ''):
        """ 加载类

        @params strModelName string 类名
        """
        #model = importlib.import_module('model.' + strModelName)

        try:
            model = importlib.import_module('model.' + strModelName)
            return model.model(self.model)
        except Exception, e:
            print e
            return None


    def importService(self, strServiceName, strServiceDir = ''):
        """ 加载Service

        @params strServiceName string Service类名
        @params strServiceDir string Service类所在目录
        """

        try:
            service = importlib.import_module('service.' + strServiceName)
            return service.service(self.model)
        except Exception, e:
            print e
            return None
            
    def formatTime(self, intTime, strTime = '%Y-%m-%d %H:%I:%M'):
        """ 将时间戳格式化为时间
        """

        return self.time.strftime(strTime, self.time.localtime(intTime))

    def timetostr(self, strDate):
        """ 将日期时间转为时间戳

        @params strDate string 日期时间
        """

        try:
            time = self.time.strptime(strDate, "%m/%d/%Y %H:%M:%S")
        except:
            time = self.time.strptime(strDate, "%Y-%m-%d %H:%M:%S")

        return int(self.time.mktime(time))
        
    def salt(self, intSaltLen = 6):
        """ 密码加密字符串
        生成一个固定位数的随机字符串，包含0-9a-z

        @params intSaltLen int 生成字符串长度
        """

        strChrset = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWSYZ'
        lisSalt = []
        for i in range(intSaltLen):
            strItem = random.choice(strChrset)
            lisSalt.append(strItem)

        strSalt = ''.join(lisSalt)
        return strSalt
        
    def getAvatarUrl(self, strCode, strType = 'avatar'):
        """ 
        """

        return '%s%s%s' % (self.dicConfig['PIC']['HOST'], strCode, '-' + strType)

    def escapeString(self, data, un = None):
        """ 特殊字符转义

        @params data string, tuple, list, dict 转义数据
        """

        if isinstance(data, str):
            return tornado.escape.xhtml_escape(data) if not un else tornado.escape.xhtml_unescape(data)
        elif isinstance(data, tuple) or isinstance(data, list):
            lisData = []
            for item in data:
                lisData.append(tornado.escape.xhtml_escape(str(item)) if not un else tornado.escape.xhtml_unescape(str(item)))

            return lisData
        elif isinstance(data, dict):
            for key in data:
                data[key] = tornado.escape.xhtml_escape(str(data[key])) if not un else tornado.escape.xhtml_unescape(str(data[key]))

            return data

    
            




