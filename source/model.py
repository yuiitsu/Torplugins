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
			self.cursor = self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)


	def find(self, strTableName, strType, dicData, booFormatData = True):
		''' 读取一组数据

		@params strTableName string 表名
		@params strType string 类型，可以是list, first
		@prams dicData dict 数据字典
		@params booFormatData bool 是否格式化数据，默认为True
		'''

		if booFormatData:
			dicData = self.formatData(dicData)

		strTableName = self.buildTableName(strTableName)
		
		strFields = self.buildFields(dicData['fields'])

		strCondition = self.buildCondition(dicData['condition'])

		strJoin = self.buildJoin(dicData['join'])

		strLimit = self.buildLimit(dicData['limit'])

		strOrder = self.buildOrder(dicData['order'])

		strSql = "select %s from %s %s %s %s %s" % (strFields, strTableName, strJoin, strCondition, strOrder, strLimit)
		#print strSql
		
		self.cursor.execute(strSql)

		if strType == 'list':
			dicList = self.cursor.fetchall()
		else:
			dicList = self.cursor.fetchone()

		return dicList


	def paginate(self, strTableName, dicData):
		''' 分页读取数据

		@params strTableName string 表名
		@params dicData dict 数据字典，可以包裹field, fields, condition等key
		'''

		dicData = self.formatData(dicData)

		# 页码
		intPage = dicData['page'] if dicData.has_key('page') else 1
		intPageNum = dicData['limit'][1] if dicData.has_key('limit') else ''
		intStartLimit = (intPage - 1) * int(intPageNum)

		dicData['limit'] = [str(intStartLimit), intPageNum]

		# 总条数
		intRows = self.getRows(strTableName, {
			'fields': ['count(*) as count'],
			'condition': dicData['condition'],
			'join': dicData['join']
		}, False)

		# 获取数据
		tupList = self.find(strTableName, 'list', dicData, False)

		return [tupList, intRows]

	def getRows(self, strTableName, dicData, booFormatData = True):
		''' 获取数据记录数

		@params strTableName string 表名
		@params dicData dict 数据字典
		@params booFormatData bool 是否格式化数据，默认为True
		'''

		if booFormatData:
			dicData = self.formatData(dicData)

		strTableName = self.buildTableName(strTableName)

		strFields = self.buildFields(dicData['fields'])

		strJoin = self.buildJoin(dicData['join'])

		strCondition = self.buildCondition(dicData['condition'])

		strSql = "select %s from %s %s %s" % (strFields, strTableName, strJoin, strCondition)
		#print strSql

		self.cursor.execute(strSql)

		dicRows = self.cursor.fetchone()

		return dicRows['count'] if dicRows else 0


	def insert(self, strTableName, dicData):
		''' 插入数据
		
		@params strTableName string 表名
		@params dicData dict 数据字典
		'''
		dicData = self.formatData(dicData)
		strTableName = self.buildTableName(strTableName)

		# 插入多条（待完）
		#if type(dicData['val']) == list:
		#	print ','.join(str(dicData['val']))


		strSql = "insert into %s (%s) values (%s)" % (strTableName, dicData['key'], dicData['val'])
		self.cursor.execute(strSql)


	def update(self, strTableName, dicData):
		''' 修改数据
		
		@params strTableName string 表名
		@params dicData dict 数据字典
		'''
		
		dicData = self.formatData(dicData)
		strTableName = self.buildTableName(strTableName)
		strFields = self.buildFields(dicData['fields'])
		strCondition = self.buildCondition(dicData['condition'])
		
		strSql = "update %s set %s %s" % (strTableName, strFields, strCondition)
		self.cursor.execute(strSql)


	def delete(self, strTableName, dicData):
		''' 删除数据
		
		@params strTableName string 表名
		@params dicData dict 数据字典
		'''

		dicData = self.formatData(dicData)
		strTableName = self.buildTableName(strTableName)
		strCondition = self.buildCondition(dicData['condition'])
		
		strSql = "delete from %s %s" % (strTableName, strCondition)
		self.cursor.execute(strSql)


	def formatData(self, dicData):
		''' 格式化数据
		将fields, condition, join 等数据格式化返回

		@params dicData dict 数据字典
		'''

		# fileds
		dicData['fields'] = dicData['fields'] if dicData.has_key('fields') else ''
		
		# join
		dicData['join'] = dicData['join'] if dicData.has_key('join') else ''

		# conditon
		dicData['condition'] = dicData['condition'] if dicData.has_key('condition') else ''

		# order
		dicData['order'] = dicData['order'] if dicData.has_key('order') else ''

		# limit
		dicData['limit'] = dicData['limit'] if dicData.has_key('limit') else ''

		# key
		dicData['key'] = dicData['key'] if dicData.has_key('key') else ''

		# val
		dicData['val'] = dicData['val'] if dicData.has_key('val') else ''


		return dicData


	def buildTableName(self, strTableName):
		''' 构建表名
		根据配置文件中的表前辍，构建表名

		@params strTableName string 表名
		'''

		strTableName = CONF['DB_TABLEPRE'] + strTableName if CONF['DB_TABLEPRE'] else strTableName

		return strTableName

	
	def buildFields(self, lisFields):
		''' 构建读取字段

		@params lisFields list 字段列表
		'''
		
		strFields = ','.join(lisFields) if lisFields else '*'

		return strFields
		
		
	def buildJoin(self, strJoin):
		''' 构建Join

		@params dicCondition dict 条件字典
		'''

		return 'LEFT JOIN %s' % strJoin if strJoin else ''


	def buildCondition(self, strCondition):
		''' 构建条件

		@params dicCondition dict 条件字典
		'''

		return 'where %s' % strCondition

	
	def buildOrder(self, strOrder):
		''' 构建order
		未完成

		@params
		'''

		#strOrder = strOrder

		return 'order by ' + strOrder if strOrder else ''


	def buildLimit(self, lisLimit):
		''' 构建limit

		@params lisLimit list limit
		'''

		strLimit = ','.join(lisLimit) if lisLimit else ''

		return 'limit ' + strLimit if strLimit else ''


	def escapeString(self, dicData):
		if dicData:
			if isinstance(dicData, dict) == False:
				#print dicData
				if type(dicData) == str or type(dicData) == unicode:
					dicData = dicData.encode('utf8')
				return MySQLdb.escape_string(dicData)
			else:
				for k, v in dicData.iteritems():
					#print type(v)
					if type(v) == str or type(v) == unicode:
						v = v.encode('utf8')
					#print v

					dicData[k] = MySQLdb.escape_string(str(v))
					#dicData[k] = str(v).replace('\'', '\\\'').replace('"', '\"')
				#exit()
				return dicData
		return False


	def __del__(self):

		if CONF['isDataBase']:
			self.db.close()
