#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 路由配置
# 增加控制器, 导入控制器文件引用类，并修改route list

import tornado.web

from conf.config import CONF

# 首页控制器
from controller.index import index

# 新的控制器写这里
# ...

route = [
	(r"/", index),
	(r"/static/(.*)", tornado.web.StaticFileHandler, dict(path = CONF['static_path'])),
]

setting = CONF
