# -*- coding:utf-8 -*-

from base import Base


# 错误处理
class Error(Base):

    def initialize(self):
        Base.initialize(self)

    def get(self):
        self.send_error(404, traceback_error="")

    def post(self):
        self.send_error(404, traceback_error="")
