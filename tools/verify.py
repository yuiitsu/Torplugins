# -*- coding:utf-8 -*-

"""
@author: zzx
@file: schedule_utils.py
@time: 17/5/2 下午4:11
"""
import re


class Verify(object):

    @staticmethod
    def ismobile(mobile_no):
        """
         测试手机号是否违法
         :param params: 
         :return boolean: 
         """
        phone_re = re.compile(r'^1[34578]\d{9}$')
        if not phone_re.match(mobile_no):
            return False
        else:
            return True

    @staticmethod
    def isemail(email):
        """
         测试手机号是否违法
         :param params: 
         :return boolean: 
         """
        if re.match(r'^(.+@\w+\.\w{2,4})$', email):
            return True
        else:
            return False

    @staticmethod
    def is_id_card(id_card):
        if re.match(r'(^[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$)|(^[1-9]\d{5}\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{2}[0-9Xx]$)', id_card):
            return True
        return False

if __name__ == "__main__":
    print Verify.is_id_card('420281199010044620')