# -*- coding:utf-8 -*-

from base import base

# 首页
class index(base):

    def initialize(self):

        # 加载父类初始化方法 
        base.initialize(self)

    # 首页面板数据
    def index(self):

        str_signature = self.I('signature')
        str_timestamp = self.I('timestamp')
        str_nonce = self.I('nonce')
        str_echostr = self.I('echostr')

        str_token = 'mw0I0hifYcr6iaqWKvesMM8wUZIMiB7f'
        lis_tmp = sorted([str_token, str_timestamp, str_nonce])
        str_tmp = self.sha1(''.join(lis_tmp))

        if str_tmp == str_signature:
            print str_echostr
            self.write(str_echostr)
        else:
            print 'error'
            self.write('error')

