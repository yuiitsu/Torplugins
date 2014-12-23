# -*- coding:utf-8 -*-

import MySQLdb
from conf.config import CONF

class baseModel(object):
	''' 数据类
	'''

	def __init__(self):
		''' 初始化
		'''

		if CONF['isDataBase']:
			strDbHost = CONF['DB_HOST']
			strDbUser = CONF['DB_USER']
			strDbPass = CONF['DB_PASS']
			strDbBase = CONF['DB_BASE']

			# 连接MYSQL
			self.db = MySQLdb.connect(strDbHost, strDbUser, strDbPass, strDbBase, use_unicode = 1, charset = 'utf8')
			self.cursor = self.db.cursor()



	def __del__(self):

		if CONF['isDataBase']:
			self.db.close()
