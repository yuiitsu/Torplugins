# -*- coding:utf-8 -*-

import redis
from source.properties import Properties
from tools.logs import Logs

properties = Properties()


class RedisBase(object):

    pool = redis.ConnectionPool(
        host=properties.get("redis", "REDIS_HOST"),
        port=properties.get("redis", "REDIS_PORT"),
        password=properties.get("redis", "REDIS_PASS"),
        decode_responses=True,
        max_connections=1000
    )

    logger = Logs().logger

    def get_conn(self):
        return redis.StrictRedis(connection_pool=self.pool)

    def set_value(self, key, value):
        try:
            resource = self.get_conn()
            resource.set(key, value)
        except Exception as e:
            self.logger.exception(e)

    def set(self, key, value, second=0):
        try:
            resource = self.get_conn()
            if second > 0:
                resource.setex(key, second, value)
            else:
                resource.set(key, value)
        except Exception as e:
            self.logger.exception(e)

    def get(self, key):
        try:
            resource = self.get_conn()
            return resource.get(key)
        except Exception as e:
            self.logger.exception(e)

    def delete(self, *key):
        result = None
        try:
            resource = self.get_conn()
            result = resource.delete(*key)
        except Exception as e:
            self.logger.exception(e)
        return result

    def hmset(self, key, value, second=0):
        try:
            resource = self.get_conn()
            with resource.pipeline() as pipe:
                pipe.hmset(key, value)
                if second > 0:
                    pipe.expire(key, int(second))
                pipe.execute()
        except Exception as e:
            self.logger.exception(e)

    def hgetall(self, key):
        try:
            resource = self.get_conn()
            return resource.hgetall(key)
        except Exception as e:
            self.logger.exception(e)

    def mget(self, key):
        try:
            resource = self.get_conn()
            return resource.mget(key)
        except Exception as e:
            self.logger.exception(e)

    def ttl(self, key):
        try:
            resource = self.get_conn()
            return resource.ttl(key)
        except Exception as e:
            self.logger.exception(e)

    def expire(self, key, second=0):
        try:
            resource = self.get_conn()
            return resource.expire(key, int(second))
        except Exception as e:
            self.logger.exception(e)

    def incr(self, key, amount=1):
        try:
            resource = self.get_conn()
            return resource.incr(key, amount)
        except Exception as e:
            self.logger.exception(e)

    def decr(self, key, amount=1):
        try:
            resource = self.get_conn()
            return resource.decr(key, amount)
        except Exception as e:
            self.logger.exception(e)

    def sadd(self, key, value):
        try:
            resource = self.get_conn()
            return resource.sadd(key, value)
        except Exception as e:
            self.logger.exception(e)

    def srem(self, key, value):
        try:
            resource = self.get_conn()
            return resource.srem(key, value)
        except Exception as e:
            self.logger.exception(e)

    def smembers(self, key):
        try:
            resource = self.get_conn()
            return resource.smembers(key)
        except Exception as e:
            self.logger.exception(e)

    def spop(self, key):
        try:
            resource = self.get_conn()
            return resource.spop(key)
        except Exception as e:
            self.logger.exception(e)

    def srem(self, key, value):
        try:
            resource = self.get_conn()
            return resource.srem(key, value)
        except Exception as e:
            self.logger.exception(e)

    def lpush(self, key, value):
        try:
            resource = self.get_conn()
            return resource.lpush(key, value)
        except Exception as e:
            self.logger.exception(e)

    def rpush(self, key, value):
        try:
            resource = self.get_conn()
            return resource.rpush(key, value)
        except Exception as e:
            self.logger.exception(e)

    def rpop(self, key):
        try:
            resource = self.get_conn()
            return resource.rpop(key)
        except Exception as e:
            self.logger.exception(e)
            raise e

    def llen(self, key):
        try:
            resource = self.get_conn()
            return resource.llen(key)
        except Exception as e:
            self.logger.exception(e)

    def lrange(self, key, start, end):
        try:
            resource = self.get_conn()
            return resource.lrange(key, start, end)
        except Exception as e:
            self.logger.exception(e)

    def hincrby(self, key, field, increment=1):
        try:
            resource = self.get_conn()
            return resource.hincrby(key, field, increment)
        except Exception as e:
            self.logger.exception(e)

    def hget(self, key, field):
        try:
            resource = self.get_conn()
            return resource.hget(key, field)
        except Exception as e:
            self.logger.exception(e)

    def hset(self, key, field, value):
        try:
            resource = self.get_conn()
            return resource.hset(key, field, value)
        except Exception as e:
            self.logger.exception(e)

    def hdel(self, key, field):
        try:
            resource = self.get_conn()
            return resource.hdel(key, field)
        except Exception as e:
            self.logger.exception(e)

    def scard(self, key):
        try:
            resource = self.get_conn()
            return resource.scard(key)
        except Exception as e:
            self.logger.exception(e)
