# -*- coding: utf-8 -*-

"""
@author: Yuiitsu
@file: shopping_cart
@time: 2018/8/20 15:42
"""
from test.tester import Tester


class T(Tester):

    def query(self):
        self.path = 'v1.example.service'
        self.method = 'query'
        self.params = {
        }


if __name__ == '__main__':
    t = T()
    t.run('query')
