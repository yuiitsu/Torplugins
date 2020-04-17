# -*- coding:utf-8 -*-

"""
@author onlyfu
@time 2018/04/02
"""
import json
import tornado.ioloop
import tornado.gen
from src.base.service import ServiceBase
from tools.date_json_encoder import CJsonEncoder
from tools.logs import Logs


class Tester(object):

    path = ''
    method = ''
    params = {}
    logger = Logs().logger

    @tornado.gen.coroutine
    def main(self):
        try:
            result = yield ServiceBase().do_service(self.path, self.method, self.params)
            print(json.dumps(result, cls=CJsonEncoder, ensure_ascii=False))
        except Exception as e:
            self.logger.exception(e)

    def run(self, func):
        """
        :param func:
        :return:
        """
        f = eval('self.' + func)
        f()
        return tornado.ioloop.IOLoop.current().run_sync(self.main)


if __name__ == '__main__':
    tester = Tester()
    tornado.ioloop.IOLoop.current().run_sync(tester.main)
