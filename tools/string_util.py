# -*- coding:utf-8 -*-

"""
@author: delu
@file: wmb2c_string_util.py
@time: 17/4/14 上午11:01
"""


class StringUtils(object):

    @staticmethod
    def money2int(text='', to_cent=True):
        """
        金额字符串转int类型
        :param text:
        :param to_cent:
        :return:
        """
        if not isinstance(text, str):
            text = str(text)
        num = 0
        if text:
            if not to_cent:
                return int(text.split('.')[0])
            else:
                num_list = text.split('.')
                num += int(num_list[0]) * 100
                if len(num_list) >= 2:
                    deci = num_list[1] + '00'
                    deci = deci[0: 2]
                    num += int(deci)
            return num
        return False


if __name__ == '__main__':
    s = StringUtils()
    print s.money2int(1.134, to_cent=False)
