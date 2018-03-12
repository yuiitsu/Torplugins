# -*- coding:utf-8 -*-

"""
@author: wsy
@file: tornado_redis.py
@time: 2017/7/13 10:04
"""

import tornadoredis
import tornado.gen
from source.properties import Properties

properties = Properties()


class AsyncRedis(object):
    # 设置连接池
    CONNECTION_POOL = tornadoredis.ConnectionPool(max_connections=int(properties.get('redis', 'REDIS_MAX_CONNNECTION')),
                                                  wait_for_available=True,
                                                  host=properties.get("redis", "REDIS_HOST"),
                                                  port=int(properties.get('redis', 'REDIS_PORT')))

    @tornado.gen.coroutine
    def get_conn(self):
        """
        获取redis客户端链接
        :return: 
        """
        resource = tornadoredis.Client(connection_pool=self.CONNECTION_POOL)
        raise tornado.gen.Return(resource)

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
        try:
            # 使用管道设置值
            resource = yield self.get_conn()
            with resource.pipeline() as pipe:
                pipe.set(key, value)
                if second > 0:
                    pipe.expire(key, int(second))

                yield tornado.gen.Task(pipe.execute)
        except Exception, e:
            print e
        finally:
            yield tornado.gen.Task(resource.disconnect)

    @tornado.gen.coroutine
    def get(self, key):
        """
        获取内存数据
        :param key: 
        :return: 
        """
        resource = None
        value = None
        try:
            resource = yield self.get_conn()
            value = yield tornado.gen.Task(resource.get, key)
        except Exception, e:
            print e
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
        try:
            # 使用管道设置值
            resource = yield self.get_conn()
            with resource.pipeline() as pipe:
                pipe.hmset(key, value)
                if second > 0:
                    pipe.expire(key, int(second))

                yield tornado.gen.Task(pipe.execute)
        except Exception, e:
            print e
        finally:
            yield tornado.gen.Task(resource.disconnect)

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
            resource = yield self.get_conn()
            value = yield tornado.gen.Task(resource.hgetall, key)
        except Exception, e:
            print e
        finally:
            yield tornado.gen.Task(resource.disconnect)
            raise tornado.gen.Return(value)

    @tornado.gen.coroutine
    def mget(self, key):
        resource = None
        value = None
        try:
            resource = yield self.get_conn()
            value = yield tornado.gen.Task(resource.mget, key)
        except Exception, e:
            print e
        finally:
            yield tornado.gen.Task(resource.disconnect)
            raise tornado.gen.Return(value)

    @tornado.gen.coroutine
    def ttl(self, key):
        """
        :author: onlyfu
        :param key:
        :return:
        """
        resource = None
        value = None
        try:
            resource = yield self.get_conn()
            value = yield tornado.gen.Task(resource.ttl, key)
        except Exception, e:
            print e
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
        resource = None
        try:
            # 使用管道设置值
            resource = yield self.get_conn()
            yield tornado.gen.Task(resource.expire, key, int(second))
        except Exception, e:
            print e
        finally:
            yield tornado.gen.Task(resource.disconnect)

    @tornado.gen.coroutine
    def incr(self, key, amount=1):
        resource = None
        value = 0
        try:
            # 使用管道设置值
            resource = yield self.get_conn()
            value = yield tornado.gen.Task(resource.incrby, key, amount)
        except Exception, e:
            print e
        finally:
            yield tornado.gen.Task(resource.disconnect)
            raise tornado.gen.Return(value)

    @tornado.gen.coroutine
    def decr(self, key, amount=1):
        resource = None
        value = 0
        try:
            # 使用管道设置值
            resource = yield self.get_conn()
            value = yield tornado.gen.Task(resource.decrby, key, amount)
        except Exception, e:
            print e
        finally:
            yield tornado.gen.Task(resource.disconnect)
            raise tornado.gen.Return(value)

    @tornado.gen.coroutine
    def sadd(self, key, value):
        resource = None
        try:
            # 使用管道设置值
            resource = yield self.get_conn()
            yield tornado.gen.Task(resource.sadd, key, value)
        except Exception, e:
            print e
        finally:
            yield tornado.gen.Task(resource.disconnect)

    @tornado.gen.coroutine
    def smembers(self, key):
        resource = None
        value = None
        try:
            resource = yield self.get_conn()
            value = yield tornado.gen.Task(resource.smembers, key)
        except Exception, e:
            print e
        finally:
            yield tornado.gen.Task(resource.disconnect)
            raise tornado.gen.Return(value)

    @tornado.gen.coroutine
    def spop(self, key):
        resource = None
        value = None
        try:
            resource = yield self.get_conn()
            value = yield tornado.gen.Task(resource.spop, key)
        except Exception, e:
            print e
        finally:
            yield tornado.gen.Task(resource.disconnect)
            raise tornado.gen.Return(value)

    @tornado.gen.coroutine
    def delete(self, key):
        """
        删除内存中值
        :param key: 
        :return: 
        """
        resource = None
        try:
            resource = yield self.get_conn()
            with resource.pipeline() as pipe:
                pipe.delete(key)
                yield tornado.gen.Task(pipe.execute)
        except Exception, e:
            print e
        finally:
            yield tornado.gen.Task(resource.disconnect)

    @tornado.gen.coroutine
    def lpush(self, key, value):
        resource = None
        try:
            # 使用管道设置值
            resource = yield self.get_conn()
            yield tornado.gen.Task(resource.lpush, key, value)
        except Exception, e:
            print e
        finally:
            yield tornado.gen.Task(resource.disconnect)
