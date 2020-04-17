# -*- coding:utf-8 -*-
"""
空路由错误处理，访问不存在地址时生效
"""

from base.base import Base


class Error(Base):

    def initialize(self):
        Base.initialize(self)

    def get(self):
        self.send_error(404, traceback_error="")

    def post(self):
        self.send_error(404, traceback_error="")
