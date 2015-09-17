#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 路由配置
# 增加控制器, 导入控制器文件引用类，并修改route list

import tornado.web

import config as config

# 自定义控制器，增加路由
import source.controller as controller
import controller.index as index
import controller.error as Error

route = [
	(r"/", index.index),
	(r".*", Error.error),
	(r"/static/(.*)", tornado.web.StaticFileHandler, dict(path = config.CONF['static_path'])),
]

setting = config.CONF
