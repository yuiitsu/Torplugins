#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 入口文件
# 通过conf/route.py文件来配置路由

import tornado.ioloop
import tornado.web

from conf.route import route, setting

app = tornado.web.Application(route, **setting)

app.listen(8888)
tornado.ioloop.IOLoop.instance().start()
