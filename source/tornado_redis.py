# -*- coding:utf-8 -*-

"""
@author: wsy
@file: tornado_redis.py
@time: 2017/7/13 10:04
"""

import tornadoredis
import tornado.gen
from source.properties import Properties
from tools.logs import Logs

properties = Properties()
logger = Logs().logger

REDIS_HOST = properties.get("redis", "REDIS_HOST")
REDIS_PORT = int(properties.get('redis', 'REDIS_PORT'))
REDIS_PASS = properties.get('redis', 'REDIS_PASS')
REDIS_MAX_CONNECTION = int(properties.get('redis', 'REDIS_MAX_CONNECTION'))


class AsyncRedis:
    # 设置连接池
    CONNECTION_POOL = tornadoredis.ConnectionPool(
        max_connections=REDIS_MAX_CONNECTION,
        wait_for_available=True,
        host=REDIS_HOST,
        port=REDIS_PORT
    )

    def get_conn(self):
        """
        获取redis客户端链接
        :return: 
        """
        resource = tornadoredis.Client(
            connection_pool=self.CONNECTION_POOL,
            password=REDIS_PASS
        )
        return resource

    @tornado.gen.coroutine
    def set(self, key, value, second=0):
        """
        存储数据
        :param key: 
        :param value: 
        :param second:
        :return:
        """
        resource = None
        result = False
        try:
            # 使用管道设置值
            resource = self.get_conn()
            with resource.pipeline() as pipe:
                pipe.set(key, value)
                if second > 0:
                    pipe.expire(key, int(second))

                result = yield tornado.gen.Task(pipe.execute)
        except Exception as e:
            logger.exception(e)
        finally:
            yield tornado.gen.Task(resource.disconnect)
            raise tornado.gen.Return(result)

    @tornado.gen.coroutine
    def get(self, key):
        """
        获取内存数据
        :param key: 
        :return: 
        """
        try:
            resource = self.get_conn()
            value = yield tornado.gen.Task(resource.get, key)
        except Exception as e:
            logger.exception(e)
        finally:
            yield tornado.gen.Task(resource.disconnect)
            raise tornado.gen.Return(value)

    @tornado.gen.coroutine
    def exists(self, key):
        """
        查询值是否存在
        :param key:
        :return:
        """
        resource = None
        value = False
        try:
            resource = self.get_conn()
            value = yield tornado.gen.Task(resource.exists, key)
        except Exception as e:
            logger.exception(e)
        finally:
            yield tornado.gen.Task(resource.disconnect)
            raise tornado.gen.Return(value)

    @tornado.gen.coroutine
    def hmget(self, key, fields):
        """
        批量获取map中指定区域的值
        :param key:
        :param fields
        :return:
        """
        resource = None
        value = False
        try:
            resource = self.get_conn()
            value = yield tornado.gen.Task(resource.hmget, key, fields)
        except Exception as e:
            logger.exception(e)
        finally:
            yield tornado.gen.Task(resource.disconnect)
            raise tornado.gen.Return(value)

    @tornado.gen.coroutine
    def hmset(self, key, value, second=0):
        """
        :author: onlyfu
        :param key:
        :param value:
        :param second:
        :return:
        """
        resource = None
        result = False
        try:
            # 使用管道设置值
            resource = self.get_conn()
            with resource.pipeline() as pipe:
                pipe.hmset(key, value)
                if second > 0:
                    pipe.expire(key, int(second))

                result = yield tornado.gen.Task(pipe.execute)
        except Exception as e:
            logger.exception(e)
        finally:
            yield tornado.gen.Task(resource.disconnect)
            raise tornado.gen.Return(result)

    @tornado.gen.coroutine
    def hset(self, key, field, value):
        """
        :author: maozhufeng
        :param key: redis键值
        :param field: hashmap中键值
        :param value:
        :return:
        """
        resource = None
        result = False
        try:
            # 使用管道设置值
            resource = self.get_conn()
            with resource.pipeline() as pipe:
                pipe.hset(key, field, value)
                result = yield tornado.gen.Task(pipe.execute)
        except Exception as e:
            logger.exception(e)
        finally:
            yield tornado.gen.Task(resource.disconnect)
            raise tornado.gen.Return(result)

    @tornado.gen.coroutine
    def hget(self, key, field):
        """
        :author: maozhufeng
        :param key: redis键值
        :param field: hashmap中键值
        :return:
        """
        resource = None
        result = None
        try:
            # 使用管道设置值
            resource = self.get_conn()
            with resource.pipeline() as pipe:
                pipe.hget(key, field)
                result = yield tornado.gen.Task(pipe.execute)
        except Exception as e:
            logger.exception(e)
        finally:
            yield tornado.gen.Task(resource.disconnect)
            if isinstance(result, list):
                result = result[0]
            raise tornado.gen.Return(result)

    @tornado.gen.coroutine
    def hdel(self, key, field, *args):
        """
        :author: maozhufeng
        :param key: redis键值
        :param field: hashmap中键值
        :return:
        """
        resource = None
        result = None
        try:
            # 使用管道设置值
            resource = self.get_conn()
            with resource.pipeline() as pipe:
                pipe.hdel(key, field, args)
                result = yield tornado.gen.Task(pipe.execute)
        except Exception as e:
            logger.exception(e)
        finally:
            yield tornado.gen.Task(resource.disconnect)
            if isinstance(result, list):
                result = result[0]
            raise tornado.gen.Return(result)

    @tornado.gen.coroutine
    def hgetall(self, key):
        """
        :author: onlyfu
        :param key:
        :return:
        """
        resource = None
        value = None
        try:
            resource = self.get_conn()
            value = yield tornado.gen.Task(resource.hgetall, key)
        except Exception as e:
            logger.exception(e)
        finally:
            yield tornado.gen.Task(resource.disconnect)
            raise tornado.gen.Return(value)

    @tornado.gen.coroutine
    def hincrby(self, key, field, increment=1):
        """
        :author: onlyfu
        :param key:
        :return:
        """
        resource = None
        value = None
        try:
            resource = self.get_conn()
            value = yield tornado.gen.Task(resource.hincrby, key, field, increment)
        except Exception as e:
            logger.exception(e)
        finally:
            yield tornado.gen.Task(resource.disconnect)
            raise tornado.gen.Return(value)

    @tornado.gen.coroutine
    def mget(self, key):
        resource = None
        value = None
        try:
            resource = self.get_conn()
            value = yield tornado.gen.Task(resource.mget, key)
        except Exception as e:
            logger.exception(e)
        finally:
            yield tornado.gen.Task(resource.disconnect)
            raise tornado.gen.Return(value)

    @tornado.gen.coroutine
    def ttl(self, key):
        """
        :author: onlyfu
        if key not exist return None
        :param key:
        :return:
        """
        resource = None
        value = -2
        try:
            resource = self.get_conn()
            value = yield tornado.gen.Task(resource.ttl, key)
            value = -1 if value is None else value
        except Exception as e:
            logger.exception(e)
        finally:
            yield tornado.gen.Task(resource.disconnect)
            raise tornado.gen.Return(value)

    @tornado.gen.coroutine
    def expire(self, key, second=0):
        """
        :author: onlyfu
        :param key:
        :param second:
        :return:
        """
        result = False
        resource = None
        try:
            # 使用管道设置值
            resource = self.get_conn()
            result = yield tornado.gen.Task(resource.expire, key, int(second))
        except Exception as e:
            logger.exception(e)
        finally:
            yield tornado.gen.Task(resource.disconnect)
            raise tornado.gen.Return(result)

    @tornado.gen.coroutine
    def incr(self, key, amount=1):
        resource = None
        value = 0
        try:
            # 使用管道设置值
            resource = self.get_conn()
            value = yield tornado.gen.Task(resource.incrby, key, amount)
        except Exception as e:
            logger.exception(e)
        finally:
            yield tornado.gen.Task(resource.disconnect)
            raise tornado.gen.Return(value)

    @tornado.gen.coroutine
    def decr(self, key, amount=1):
        resource = None
        value = 0
        try:
            # 使用管道设置值
            resource = self.get_conn()
            value = yield tornado.gen.Task(resource.decrby, key, amount)
        except Exception as e:
            logger.exception(e)
        finally:
            yield tornado.gen.Task(resource.disconnect)
            raise tornado.gen.Return(value)

    @tornado.gen.coroutine
    def sadd(self, key, value, *args):
        resource = None
        # 未操作成功默认返回0，操作成功返回1
        result = 0
        try:
            # 使用管道设置值
            resource = self.get_conn()
            result = yield tornado.gen.Task(resource.sadd, key, value, *args)
        except Exception as e:
            logger.exception(e)
        finally:
            yield tornado.gen.Task(resource.disconnect)
            raise tornado.gen.Return(result)

    @tornado.gen.coroutine
    def scard(self, key):
        resource = None
        # 未操作成功默认返回0
        result = 0
        try:
            # 使用管道设置值
            resource = self.get_conn()
            result = yield tornado.gen.Task(resource.scard, key)
        except Exception as e:
            logger.exception(e)
        finally:
            yield tornado.gen.Task(resource.disconnect)
            raise tornado.gen.Return(result)

    @tornado.gen.coroutine
    def smembers(self, key):
        resource = None
        value = None
        try:
            resource = self.get_conn()
            value = yield tornado.gen.Task(resource.smembers, key)
        except Exception as e:
            logger.exception(e)
        finally:
            yield tornado.gen.Task(resource.disconnect)
            raise tornado.gen.Return(value)

    @tornado.gen.coroutine
    def spop(self, key):
        resource = None
        value = None
        try:
            resource = self.get_conn()
            value = yield tornado.gen.Task(resource.spop, key)
        except Exception as e:
            logger.exception(e)
        finally:
            yield tornado.gen.Task(resource.disconnect)
            raise tornado.gen.Return(value)

    @tornado.gen.coroutine
    def srem(self, key, value):
        resource = None
        result = None
        try:
            resource = self.get_conn()
            result = yield tornado.gen.Task(resource.srem, key, value)
        except Exception as e:
            logger.exception(e)
        finally:
            yield tornado.gen.Task(resource.disconnect)
            raise tornado.gen.Return(result)

    @tornado.gen.coroutine
    def delete(self, key, *args):
        """
        删除内存中值
        :param key: 
        :return: 
        """
        resource = None
        result = False
        try:
            resource = self.get_conn()
            with resource.pipeline() as pipe:
                pipe.delete(key, *args)
                result = yield tornado.gen.Task(pipe.execute)
        except Exception as e:
            logger.exception(e)
        finally:
            yield tornado.gen.Task(resource.disconnect)
            raise tornado.gen.Return(result)

    @tornado.gen.coroutine
    def lpush(self, key, value, *args):
        resource = None
        result = 0
        try:
            # 使用管道设置值
            resource = self.get_conn()
            result = yield tornado.gen.Task(resource.lpush, key, value, *args)
        except Exception as e:
            logger.exception(e)
        finally:
            yield tornado.gen.Task(resource.disconnect)
            raise tornado.gen.Return(result)

    @tornado.gen.coroutine
    def rpush(self, key, value, *args):
        resource = None
        result = 0
        try:
            resource = self.get_conn()
            result = yield tornado.gen.Task(resource.rpush, key, value, *args)
        except Exception as e:
            logger.exception(e)
        finally:
            yield tornado.gen.Task(resource.disconnect)
            raise tornado.gen.Return(result)

    @tornado.gen.coroutine
    def rpop(self, key):
        resource = None
        value = None
        try:
            resource = self.get_conn()
            value = yield tornado.gen.Task(resource.rpop, key)
        except Exception as e:
            logger.exception(e)
        finally:
            yield tornado.gen.Task(resource.disconnect)
            raise tornado.gen.Return(value)

    @tornado.gen.coroutine
    def llen(self, key):
        resource = None
        value = None
        try:
            resource = self.get_conn()
            value = yield tornado.gen.Task(resource.llen, key)
        except Exception as e:
            logger.exception(e)
        finally:
            yield tornado.gen.Task(resource.disconnect)
            raise tornado.gen.Return(value)

    @tornado.gen.coroutine
    def lrange(self, key, start, end):
        resource = None
        value = None
        try:
            resource = self.get_conn()
            value = yield tornado.gen.Task(resource.lrange, key, start, end)
        except Exception as e:
            logger.exception(e)
        finally:
            yield tornado.gen.Task(resource.disconnect)
            raise tornado.gen.Return(value)
