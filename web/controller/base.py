#!usr/bin/env python
# -*- coding:utf-8 -*-

import hashlib
import json
import random
import importlib
import time
import math

import source.controller as controller
import conf.config as config

class base(controller.controller):
    """ 基类
    """

    isSign = False # 是否使用签名验证

    signPass = True # 是否通过签名验证

    isAuth = False # 是否使用登录验证

    json = json

    time = time

    dicConfig = config.CONF # 加载配置文件

    logged_user = {}


    def initialize(self):
        """ 初始化

        初始化数据类
        """

        # 设置模板目录(必须)
        self.strViewPath = self.dicConfig['VIEW_PATH']

        # 加载父类初始化方法
        controller.controller.initialize(self)

        self.dicViewData['title'] = self.dicConfig['title']
        
        # 用户登录信息
        self.login_user()

    def login_user(self):
        """ 获取用户登录信息
        """

        self.logged_user = self.current_user

        self.dicViewData['login_user'] = self.logged_user

    def auth(self):
        """ 登录认证
        读取cookie值，判断是否登录

        @params strUserName string 用户名
        """

        if not self.current_user['user_id']:
            self.redirect(self.dicConfig['login_url'])
            return
        else:
            self.login_user()

    def api_sign(self, dic_data, str_post_url):
        """ API签名请求

        @params dic_data dict 发送数据字典
        @params str_post_url string 请求地址
        """

        # 将数据json
        str_data = self.json.dumps(dic_data)

        # 生成请求时间
        str_time = str(self.time.time())

        # 进行签名加密
        str_hash = self.md5('%s%s%s' % (strData, strTime, self.dicConfig['bag_api_key']))

        # 发送请求
        str_result = self.rquest(str_post_url, 'POST', {'data': str_data, 'tamp': str_time, 'hash': str_hash})
        #print strResult.encode('utf8')

        dic_result = {}
        try:
            dic_result = self.json.loads(str_result)
        except Exception:
            return False

        return dic_result



    def md5(self, strText):
        """ MD5加密

        @params strText string 需加密字符串
        @return strResult string 加密后字符串
        """
        strResult = hashlib.md5(strText)
        return strResult.hexdigest()

    def sha1(self, strText):
        """ sha1 加密

        @params strText string 需加密字符串
        @return strResult string 加密后字符串
        """

        return hashlib.sha1(strText).hexdigest()

    def salt(self, intSaltLen = 6, isNum = False):
        """ 密码加密字符串
        生成一个固定位数的随机字符串，包含0-9a-z

        @params intSaltLen int 生成字符串长度
        """

        if isNum:
            strChrset = '0123456789'
        else:
            strChrset = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWSYZ'
        lisSalt = []
        for i in range(intSaltLen):
            strItem = random.choice(strChrset)
            lisSalt.append(strItem)

        strSalt = ''.join(lisSalt)
        return strSalt



    def out(self, statusCode, strMsg = '', dicData = {}):
        """ 输出结果

        @params statusCode int 状态值
        @params strMsg string 说明文字
        @params dicData dict 返回数据字典
        """

        dicOut = {
            'status': statusCode,
            'msg': strMsg,
            'data': dicData
        }

        self.write(json.dumps(dicOut))


    def page(self, intPage, intPageDataNum, intDataCount, strPageUrl):
        """ 分页处理

        @params intPage int 当前页码
        @params intPageDataNum int 每页多少条数据
        @params intDataCount int 共有多少条数据
        @params strPageUrl string 分页链接
        <nav>
            <ul class="pagination pull-right">
                <li><a href="#">&laquo;</a></li>
                <li class="active"><a href="#">1</a></li>
                <li><a href="#">2</a></li>
                <li><a href="#">3</a></li>
                <li><a href="#">4</a></li>
                <li><a href="#">5</a></li>
                <li><a href="#">&raquo;</a></li>
            </ul>
        </nav>
        """
        lisPageHtml = []

        intPageCount = int(math.ceil(float(intDataCount) / float(intPageDataNum)))

        if intPageCount > 1:
            lisPageHtml.append('<nav><ul class="pagination">')
            if intPage > 1:
                lisPageHtml.append('<li><a href="%s&page=%d">&laquo;</a></li>' % (strPageUrl, 1))

            if intPageCount < 10:
                for i in range(1, intPageCount + 1):
                    strClassName = 'active' if i == intPage else ''
                    strPageNum ='<li class="%s"><a href="%s&page=%d">%d</a></li>' % (strClassName, strPageUrl, i, i)
                    lisPageHtml.append(strPageNum)
            else:
                intNum = int(math.ceil(float(intPage/10) + 1 if intPage/10 == 1 else float(intPage)/10) - 1)
                if intNum == 0:
                    intStartPageNum = 1
                    intEndPageNum = 9 if intPageCount >=9 else intPageCount
                else:
                    intStartPageNum = intNum * 10
                    intEndPageNum = intNum * 10 + 9 if intPageCount >= (intNum * 10 + 9) else intPageCount
                    intMorePrePageNum = intStartPageNum - 1
                    lisPageHtml.append('<li><a href="%s&page=%d">...</a></li>' % (strPageUrl, intMorePrePageNum))

                for i in range(intStartPageNum, intEndPageNum + 1):
                    strClassName = 'active' if i == intPage else ''
                    strPageNum ='<li class="%s"><a href="%s&page=%d">%d</a></li>' % (strClassName, strPageUrl, i, i)
                    lisPageHtml.append(strPageNum)

                if intPageCount >= (intNum * 10 + 9):
                    intMoreNextPageNum = intEndPageNum + 1
                    lisPageHtml.append('<li><a href="%s&page=%d">...</a></li>' % (strPageUrl, intMoreNextPageNum))


            if intPage < intPageCount:
                lisPageHtml.append('<li><a href="%s&page=%d">&raquo;</a></li>' % (strPageUrl, intPageCount))

            lisPageHtml.append('</ul></nav>')


        strPageHtml = ''.join(lisPageHtml)
        return strPageHtml


    def formatTime(self, intTime, strTime = '%Y-%m-%d %H:%I:%M'):
        """ 将时间戳格式化为时间
        """

        return self.time.strftime(strTime, self.time.localtime(intTime))

    def timetostr(self, strDate):
        """ 将日期时间转为时间戳

        @params strDate string 日期时间
        """

        return self.time.mktime(strDate.timetuple())

    def get_current_user(self):
        """ 获取cookie值
        """

        strUserId = self.get_secure_cookie('user_id')
        intUserId = int(strUserId) if strUserId else 0

        return {
            'user_id': intUserId,
            'nickname': self.get_secure_cookie('user_nickname'),
            'avatar': self.getAvatarUrl(self.get_secure_cookie('user_avatar'))
        }

    def getAvatarUrl(self, strCode):
        """ 
        """

        return '%s%s%s' % (self.dicConfig['PIC']['HOST'], strCode, '-avatar')


    def clearTemplateCache(self):
        """ 清除模板缓存
        """

        self._template_loaders.clear()


    def get(self, **params):
        """ 重写父类get方法，接受GET请求
        增加登录验证判断

        固定参数a，如果a有值，调用同名方法，如果a没有值，调用index方法
        """

        if self.isAuth:
            self.auth()

        if not self.signPass:
            return

        controller.controller.get(self)

    def post(self):
        """ 重写父类post方法，接受POST请求
        增加登录验证判断

        固定参数a，如果a有值，调用同名方法，如果a没有值，调用index方法
        """

        if self.isAuth:
            self.auth()

        if not self.signPass:
            return

        controller.controller.post(self)






