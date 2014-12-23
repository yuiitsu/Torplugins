#!usr/bin/env python
# -*- coding:utf-8 -*-

import tornado.web
import importlib

from conf.config import CONF

class controller(tornado.web.RequestHandler):
	''' 基类
	'''

	dicViewData = {} # 模板输出数据

	dicConfig = CONF # 加载配置文件
	
	def initialize(self):
		''' 初始化

		初始化数据类
		'''

			
		# 加载Model
		try:
			model = importlib.import_module('model.' + self.__class__.__name__ + 'Model')
			self.model = model.model()
		except Exception, e:
			print e
			self.model = None

		self.dicViewData['title'] = self.dicConfig['title']
		
	
	def get(self):
		''' 接受GET请求

		固定参数a，如果a有值，调用同名方法，如果a没有值，调用index方法
		'''
	
		try:
			strAction = self.get_argument('a').strip()
		except Exception, e:
			strAction = 'index'

		if strAction:
			method = eval('self.' +strAction)
			method()
			return

	def post(self):
		''' 接受POST请求

		固定参数a，如果a有值，调用同名方法，如果a没有值，调用index方法
		'''

		try:
			strAction = self.get_argument('a').strip()
		except Exception, e:
			strAction = 'index'

		if strAction:
			method = eval('self.' +strAction)
			method()
			return


	def display(self, strViewName):
		''' 输出模板
		调用模板输出，使用当前类名为模板目录

		@params strViewName string 调用模板名称
		@params dicData dict 输出数据
		'''

		self.render("%s/%s/%s.html" % (self.dicConfig['view_dir'], self.__class__.__name__, strViewName), controller = self.__class__.__name__, data = self.dicViewData)


	def I(self, strKey):
		''' 获取请求参数
		如果只有一个值，将其转为字符串，如果是list，保留list类型

		@params strKey string 参数名称
		'''

		lisValue = self.request.arguments[strKey]

		if len(lisValue) > 1:
			return lisValue
		else:
			return lisValue[0].strip()

	def II(self, strKey):
		''' 获取请求参数
		只返回list类型

		@params strKey string 参数名称
		'''

		lisValue = self.request.arguments[strKey]

		return lisValue

