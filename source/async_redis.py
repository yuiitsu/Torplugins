# -*- coding:utf-8 -*-

"""
@package:
@file: aio_redis.py
@author: yuiitsu
@time: 2020-04-03 19:48
"""
import ssl
import aioredis
from source.properties import Properties
from tools.logs import Logs

properties = Properties()
logger = Logs().logger

REDIS_HOST = properties.get("redis", "REDIS_HOST")
REDIS_PORT = int(properties.get('redis', 'REDIS_PORT'))
REDIS_PASS = properties.get('redis', 'REDIS_PASS')
REDIS_USE_SSL = properties.get('redis', 'REDIS_USE_SSL')
REDIS_MAX_CONNECTION = int(properties.get('redis', 'REDIS_MAX_CONNECTION'))
SSLContext = ssl.SSLContext() if REDIS_USE_SSL and REDIS_USE_SSL == 'True' else False


class AsyncRedis:

    async def get_conn(self):
        """
        获取连接
        :return:
        """
        redis = await aioredis.create_redis(
            (REDIS_HOST, REDIS_PORT),
            password=REDIS_PASS,
            encoding='utf-8',
            ssl=SSLContext
        )
        return redis

    async def get(self, key):
        """
        :param key:
        :return:
        """
        r = None
        result = False
        try:
            r = await self.get_conn()
            result = await r.get(key)
        except Exception as e:
            logger.exception(e)
        finally:
            if r:
                r.close()
                await r.wait_closed()

        return result

    async def set(self, key, value, second=0):
        """
        :param key:
        :param value:
        :param second:
        :return:
        """
        r = None
        result = False
        try:
            r = await self.get_conn()
            pipe = r.pipeline()
            pipe.set(key, value)
            if second > 0:
                pipe.expire(key, int(second))

            result = await pipe.execute()
        except Exception as e:
            logger.exception(e)
        finally:
            if r:
                r.close()
                await r.wait_closed()

        return result

    async def exists(self, key):
        """
        :param key:
        :return:
        """
        r = None
        result = False
        try:
            r = await self.get_conn()
            result = await r.exists(key)
        except Exception as e:
            logger.exception(e)
        finally:
            if r:
                r.close()
                await r.wait_closed()

        return result

    async def hmget(self, key, field):
        """
        :param key:
        :param field:
        :return:
        """
        r = None
        result = False
        try:
            r = await self.get_conn()
            result = await r.hmget(key, field)
        except Exception as e:
            logger.exception(e)
        finally:
            if r:
                r.close()
                await r.wait_closed()

        return result

    async def hmset(self, key, value, second=0):
        """
        :param key:
        :param value:
        :param second:
        :return:
        """
        r = None
        result = False
        try:
            r = await self.get_conn()
            pipe = r.pipeline()
            pipe.hmset_dict(key, value)
            if second > 0:
                pipe.expire(key, int(second))

            result = await pipe.execute()
        except Exception as e:
            logger.exception(e)
        finally:
            if r:
                r.close()
                await r.wait_closed()

        return result

    async def hset(self, key, field, value):
        """
        :param key:
        :param field:
        :param value:
        :return:
        """
        r = None
        result = False
        try:
            r = await self.get_conn()
            result = await r.hset(key, field, value)
        except Exception as e:
            logger.exception(e)
        finally:
            if r:
                r.close()
                await r.wait_closed()

        return result

    async def hget(self, key, field):
        """
        :param key:
        :param field:
        :return:
        """
        r = None
        result = False
        try:
            r = await self.get_conn()
            result = await r.hget(key, field)
        except Exception as e:
            logger.exception(e)
        finally:
            if r:
                r.close()
                await r.wait_closed()

        return result

    async def hdel(self, key, field, *args):
        """
        :param key:
        :param field:
        :param args:
        :return:
        """
        r = None
        result = False
        try:
            r = await self.get_conn()
            result = await r.hdel(key, field, args)
        except Exception as e:
            logger.exception(e)
        finally:
            if r:
                r.close()
                await r.wait_closed()

        return result

    async def hgetall(self, key):
        """
        :param key:
        :return:
        """
        r = None
        result = False
        try:
            r = await self.get_conn()
            result = await r.hgetall(key)
        except Exception as e:
            logger.exception(e)
        finally:
            if r:
                r.close()
                await r.wait_closed()

        return result

    async def hincrby(self, key, field, increment=1):
        """
        :param key:
        :param field:
        :param increment:
        :return:
        """
        r = None
        result = False
        try:
            r = await self.get_conn()
            result = await r.hincrby(key, field, increment)
        except Exception as e:
            logger.exception(e)
        finally:
            if r:
                r.close()
                await r.wait_closed()

        return result

    async def mget(self, key):
        """
        :param key:
        :return:
        """
        r = None
        result = False
        try:
            r = await self.get_conn()
            result = await r.mget(*key)
        except Exception as e:
            logger.exception(e)
        finally:
            if r:
                r.close()
                await r.wait_closed()

        return result

    async def ttl(self, key):
        """
        :param key:
        :return:
        """
        r = None
        result = -2
        try:
            r = await self.get_conn()
            result = await r.ttl(key)
            result = -1 if result is None else result
        except Exception as e:
            logger.exception(e)
        finally:
            if r:
                r.close()
                await r.wait_closed()

        return result

    async def expire(self, key, second=0):
        """
        :param key:
        :param second:
        :return:
        """
        r = None
        result = None
        try:
            r = await self.get_conn()
            result = await r.expire(key, int(second))
        except Exception as e:
            logger.exception(e)
        finally:
            if r:
                r.close()
                await r.wait_closed()

        return result

    async def incr(self, key, amount=1):
        """
        :param key:
        :param amount:
        :return:
        """
        r = None
        result = None
        try:
            r = await self.get_conn()
            result = await r.incrby(key, amount)
        except Exception as e:
            logger.exception(e)
        finally:
            if r:
                r.close()
                await r.wait_closed()

        return result

    async def incrby(self, key, amount=1):
        """
        :param key:
        :param amount:
        :return:
        """
        r = None
        result = None
        try:
            r = await self.get_conn()
            result = await r.incrby(key, amount)
        except Exception as e:
            logger.exception(e)
        finally:
            if r:
                r.close()
                await r.wait_closed()

        return result

    async def decr(self, key, amount=1):
        """
        :param key:
        :param amount:
        :return:
        """
        r = None
        result = None
        try:
            r = await self.get_conn()
            result = await r.decr(key, amount)
        except Exception as e:
            logger.exception(e)
        finally:
            if r:
                r.close()
                await r.wait_closed()

        return result

    async def sadd(self, key, value, *args):
        """
        :param key:
        :param value:
        :param args:
        :return:
        """
        r = None
        result = None
        try:
            r = await self.get_conn()
            result = await r.sadd(key, value, *args)
        except Exception as e:
            logger.exception(e)
        finally:
            if r:
                r.close()
                await r.wait_closed()

        return result

    async def scard(self, key):
        """
        :param key:
        :return:
        """
        r = None
        result = None
        try:
            r = await self.get_conn()
            result = await r.scard(key)
        except Exception as e:
            logger.exception(e)
        finally:
            if r:
                r.close()
                await r.wait_closed()

        return result

    async def smembers(self, key):
        """
        :param key:
        :return:
        """
        r = None
        result = None
        try:
            r = await self.get_conn()
            result = await r.smembers(key)
        except Exception as e:
            logger.exception(e)
        finally:
            if r:
                r.close()
                await r.wait_closed()

        return result

    async def spop(self, key):
        """
        :param key:
        :return:
        """
        r = None
        result = None
        try:
            r = await self.get_conn()
            result = await r.spop(key)
        except Exception as e:
            logger.exception(e)
        finally:
            if r:
                r.close()
                await r.wait_closed()

        return result

    async def srem(self, key, value):
        """
        :param key:
        :param value:
        :return:
        """
        r = None
        result = None
        try:
            r = await self.get_conn()
            result = await r.srem(key, value)
        except Exception as e:
            logger.exception(e)
        finally:
            if r:
                r.close()
                await r.wait_closed()

        return result

    async def delete(self, *key):
        """
        :param key:
        :return:
        """
        r = None
        result = False
        try:
            r = await self.get_conn()
            result = await r.delete(*key)
        except Exception as e:
            logger.exception(e)
        finally:
            if r:
                r.close()
                await r.wait_closed()

        return result

    async def lpush(self, key, value, *args):
        """
        :param key:
        :param value:
        :param args:
        :return:
        """
        r = None
        result = None
        try:
            r = await self.get_conn()
            result = await r.lpush(key, value, *args)
        except Exception as e:
            logger.exception(e)
        finally:
            if r:
                r.close()
                await r.wait_closed()

        return result

    async def rpush(self, key, value, *args):
        """
        :param key:
        :param value:
        :param args:
        :return:
        """
        r = None
        result = None
        try:
            r = await self.get_conn()
            result = await r.rpush(key, value, *args)
        except Exception as e:
            logger.exception(e)
        finally:
            if r:
                r.close()
                await r.wait_closed()

        return result

    async def rpop(self, key):
        """
        :param key:
        :return:
        """
        r = None
        result = None
        try:
            r = await self.get_conn()
            result = await r.rpop(key)
        except Exception as e:
            logger.exception(e)
        finally:
            if r:
                r.close()
                await r.wait_closed()

        return result

    async def llen(self, key):
        """
        :param key:
        :return:
        """
        r = None
        result = None
        try:
            r = await self.get_conn()
            result = await r.llen(key)
        except Exception as e:
            logger.exception(e)
        finally:
            if r:
                r.close()
                await r.wait_closed()

        return result

    async def lrange(self, key, start, end):
        """
        :param key:
        :param start:
        :param end:
        :return:
        """
        r = None
        result = None
        try:
            r = await self.get_conn()
            result = await r.lrange(key, start, end)
        except Exception as e:
            logger.exception(e)
        finally:
            if r:
                r.close()
                await r.wait_closed()

        return result
