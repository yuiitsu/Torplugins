# -*- coding: utf-8 -*-

"""
@author: Yuiitsu
@file: async_task
@time: 2018/2/6 17:55
"""
import sys; sys.path.append('../')
import tornado.ioloop as tornado_io_loop
import tornado.gen
from v1.base.service import ServiceBase


@tornado.gen.coroutine
def main():
    yield ServiceBase().do_service('task.service', 'main_loop', {})


if __name__ == '__main__':
    # tornado_io_loop.IOLoop.current().run_sync(main)
    tornado_io_loop.IOLoop.instance().run_sync(main)
