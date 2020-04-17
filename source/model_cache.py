# -*- coding: utf-8 -*-

"""
@author: Yuiitsu
@file: cache
@time: 2018/7/12 14:11
"""
import json
import tornado.gen
from functools import wraps
from source.async_redis import AsyncRedis
from tools.date_json_encoder import CJsonEncoder
from tools.logs import Logs

redis = AsyncRedis()
logger = Logs().logger


class CacheRouter:

    @staticmethod
    @tornado.gen.coroutine
    def string_get(key, **kwargs):
        result = yield redis.get(key)
        raise tornado.gen.Return(result)

    @staticmethod
    @tornado.gen.coroutine
    def string_set(key, **kwargs):
        value = kwargs['value']
        second = kwargs['second'] if 'second' in kwargs else 0
        try:
            value = json.dumps(value, cls=CJsonEncoder)
        except Exception as e:
            logger.exception(e)

        result = yield redis.set(key, value, second)
        raise tornado.gen.Return(result)

    @staticmethod
    @tornado.gen.coroutine
    def string_del(key, **kwargs):
        result = yield redis.delete(key)
        raise tornado.gen.Return(result)

    @staticmethod
    @tornado.gen.coroutine
    def hash_m_get(key, **kwargs):
        result = yield redis.hgetall(key)
        raise tornado.gen.Return(result)

    @staticmethod
    @tornado.gen.coroutine
    # def hash_get(key, field):
    def hash_get(key, **kwargs):
        field = kwargs['field']
        result = yield redis.hget(key, field)
        raise tornado.gen.Return(result)

    @staticmethod
    @tornado.gen.coroutine
    def hash_set(key, **kwargs):
        field = kwargs['field']
        value = kwargs['value']

        try:
            value = json.dumps(value, cls=CJsonEncoder)
        except Exception as e:
            logger.exception(e)
            raise

        result = yield redis.hset(key, field, value)
        raise tornado.gen.Return(result)

    @staticmethod
    @tornado.gen.coroutine
    def hash_m_set(key, value, second):
        result = yield redis.hmset(key, value, second)
        raise tornado.gen.Return(result)

    @staticmethod
    @tornado.gen.coroutine
    def hash_del(key, **kwargs):
        field = kwargs['field']
        result = yield redis.hdel(key, field)
        raise tornado.gen.Return(result)


def get_key(args, key, field, key_after_key, field_after_key, key_pre_dict):
    if key_pre_dict:
        if (not isinstance(key_pre_dict, dict)) or (key not in key_pre_dict):
            raise ValueError

        target_key = key_pre_dict[key]
    else:
        target_key = key

    target_field = field if field else ''
    for arg in args:
        if isinstance(arg, dict):
            for k, v in arg.items():
                v = str(v)
                if k == key_after_key:
                    target_key = target_key + ":" + v

                if k == field_after_key:
                    target_field = target_field + ':' + v if target_field else v
        elif isinstance(arg, list):
            for item in arg:
                if isinstance(item, dict):
                    for k, v in item.items():
                        v = str(v)
                        if k == key_after_key:
                            target_key = target_key + ":" + v

                        if k == field_after_key:
                            target_field = target_field + ':' + v if target_field else v

    return {
        'target_key': target_key,
        'target_field': target_field
    }


def cache(data_type=None, type_method=None, key=None, field=None, key_after_key=None, field_after_key=None,
          expire=0, refresh=None, key_pre_dict=None):
    """
    缓存装饰器
    :param data_type: 缓存数据类型，用于调用对应类型的各种方法，string/hash
    :param type_method: 数据类型对应方法, None/m
    :param key: 缓存key
    :param field: hash中的key
    :param key_after_key: 缓存key后辍的key
    :param field_after_key: field后辍的key
    :param expire: 过期时间
    :param refresh: 刷新，如果为true，更新缓存数据
    :param key_pre_dict:
    :return:
    """

    def decorate(func):
        @wraps(func)
        @tornado.gen.coroutine
        def wrapper(*args, **kwargs):
            keys = get_key(args, key, field, key_after_key, field_after_key, key_pre_dict)
            target_key = keys['target_key']
            target_field = keys['target_field']

            cache_func_pre = data_type + '_' + type_method if type_method else data_type
            cache_func_str = cache_func_pre + '_get'
            if hasattr(CacheRouter, cache_func_str) and not refresh:
                cache_func = getattr(CacheRouter, cache_func_str)
                data = yield cache_func(target_key, field=target_field)

                if isinstance(data, str) and data:
                    try:
                        data = json.loads(data)
                    except Exception as e:
                        logger.exception(e)

                if data:
                    raise tornado.gen.Return(data)

            result = yield func(*args, **kwargs)
            if result:
                cache_func_str = cache_func_pre + '_set'
                if hasattr(CacheRouter, cache_func_str):
                    cache_func = getattr(CacheRouter, cache_func_str)
                    yield cache_func(target_key, field=target_field, value=result, second=expire)

            return result

        return wrapper

    return decorate


def cache_del(data_type=None, key=None, field=None, key_after_key=None, field_after_key=None, key_pre_dict=None):
    """
    删除缓存
    :param data_type:
    :param key:
    :param field:
    :param key_after_key:
    :param field_after_key:
    :param key_pre_dict:
    :return:
    """
    def decorate(func):
        @wraps(func)
        @tornado.gen.coroutine
        def wrapper(*args, **kwargs):
            keys = get_key(args, key, field, key_after_key, field_after_key, key_pre_dict)
            target_key = keys['target_key']
            target_field = keys['target_field']

            result = yield func(*args, **kwargs)
            if result:
                cache_func_str = data_type + '_del'
                if hasattr(CacheRouter, cache_func_str):
                    cache_func = getattr(CacheRouter, cache_func_str)
                    yield cache_func(target_key, field=target_field)

            return result

        return wrapper

    return decorate


class CacheTest:
    @cache(data_type="hash", key="cache:test", key_after_key="goods_id", type_method='m')
    @tornado.gen.coroutine
    def test(self, params):
        raise tornado.gen.Return(params)


if __name__ == "__main__":
    print(CacheTest().test({
        'goods_id': 'abc'
    }))
