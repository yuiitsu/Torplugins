# -*- coding:utf-8 -*-
# WEB 入口文件
# 通过web/conf/route.py文件来配置路由

import sys; sys.path.append("../")
import tornado.web

import source.controller as controller
from route import route
from conf.config import CONF

print 'server started, version: ' + CONF['version']

if __name__ == '__main__':
    controller.Server().start(route, CONF)
else:
    app = tornado.web.Application(route, **CONF)
