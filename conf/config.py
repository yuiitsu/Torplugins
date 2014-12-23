#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 配置文件

CONF = {
	# web服务端口
	'web_port': 8888,

	# 是否开启调试模式。在调试模式中，修改文件不需要重启服务，且会将错误信息输出到页面
	'debug': True,

	# COOKIE设置
	'cookie_secret': '([x4DcNKNJWsq)D-Fm#P',

	# 数据库
	'isDataBase': False, # 是否使用数据库，默认为False，开启后，请配置数据库信息
	'DB_HOST': '',
	'DB_USER': '',
	'DB_PASS': '',
	'DB_BASE': '',

	# 静太文件目录
	'static_path': 'static',

	# 登录地址 当用户未登录时，系统跳到此地址
	'login_url': '/login',
	
	# 模板设置
	'view_dir': '../view',
	
	# WEB title
	'title': 't3 tornado web',

	# 这里可以写点什么
	# ...
}
