# -*- coding:utf-8 -*-

import importlib
import sys
import traceback
import json

import tornado.escape
import tornado.gen
import tornado.ioloop
import tornado.web
import tornado.httpserver

from tools.logs import Logs


class Controller(tornado.web.RequestHandler):
    """ 
    基类
    """
    controllerKey = ''  # controller对应的key
    user_type = None
    config = None
    view_data = {}  # 模板输出数据
    model = None
    _GET = False
    _POST = False
    view_path = ''
    escape = tornado.escape
    version = ''
    importlib = importlib
    logger = Logs().logger

    def initialize(self):
        """
        初始化
        :return: 
        """
        # self.view_path = self.config['VIEW_PATH']

    def on_finish(self):
        """
        """
        # self.model.__del__()
        pass

    @tornado.gen.coroutine
    def display(self, view_name, view_path=''):
        """ 
        输出模板
        调用模板输出，使用当前类名为模板目录
        @params viewName string 调用模板名称
        @params data dict 输出数据
        """

        view_path = view_path if view_path else self.view_path

        if not self.config['debug']:
            try:
                self.render("%s/%s/%s.html" % (view_path, self.__class__.__name__, view_name),
                            controller=self.__class__.__name__, **self.view_data)
            except Exception as e:
                self.logger.exception(e)
                self.redirect('/700')
                return
        else:
            self.render("%s/%s/%s.html" % (view_path, self.__class__.__name__, view_name),
                        controller=self.__class__.__name__, **self.view_data)

    def get_params(self, key=""):
        """ 
        获取请求参数
        如果只有一个值，将其转为字符串，如果是list，保留list类型
        @:param key 参数名称
        @:param data_type 返回数据类型，默认
        """
        if not key:
            result = {}
            data = self.request.arguments
            for (k, v) in data.items():
                if len(v) > 1:
                    value_strip = []
                    for item in v:
                        value_strip.append(item.strip())
                    result[k] = value_strip
                else:
                    result[k] = v[0].strip().decode('utf-8')

            # 处理request.body数据
            if self.request.body:
                try:
                    result['request_body'] = self.request.body.decode(encoding='utf-8', errors='strict')
                    result['request_body'] = json.loads(result['request_body'])
                except Exception as e:
                    result['request_body'] = self.request.body

            return result
        else:
            try:
                value = self.request.arguments[key]
                if len(value) > 1:
                    value_strip = []
                    for item in value:
                        value_strip.append(item.strip())
                    return value_strip
                else:
                    return value[0].strip().decode('utf-8')
            except Exception as e:
                return ''

    def import_model(self, model_name):
        """ 
        加载类
        @:param model_name 类名
        @:param model_dir 目录
        """

        try:
            model = importlib.import_module(self.version + '.model.' + model_name)
            return model.Model(self.model)
        except Exception as e:
            self.logger.exception(e)
            return None

    def import_service(self, service_name):
        """ 
        加载服务类
        @params service_name 服务类名
        @params service_dir 服务类所在目录
        """

        try:
            service = importlib.import_module(self.version + '.service.' + service_name)
            return service.Service()
        except Exception as e:
            self.logger.exception(e)
            return None

    def write_error(self, status_code, **kwargs):
        """
        复写方法
        :param status_code:
        :param kwargs:
        :return:
        """
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write({
            'code': -status_code,
            'msg': '服务错误，请联系管理员',
            'traceback': kwargs['traceback_error']
        })
        self.finish()

    def send_error(self, status_code=500, **kwargs):
        """
        复写方法
        :param status_code:
        :param kwargs:
        :return:
        """
        if self._headers_written:
            # gen_log.error("Cannot send error response after headers written")
            self.logger.info('Cannot send error response after headers written')
            if not self._finished:
                self.finish()
            return
        self.clear()

        if 'exc_info' in kwargs:
            kwargs['traceback_error'] = traceback.format_exc()
        self.set_status(status_code)
        try:
            self.write_error(status_code, **kwargs)
        except Exception as e:
            self.logger.exception(e)

        if not self._finished:
            self.finish()


class server(object):
    """
    启用服务
    """

    def start(self, route, setting):

        # 获取参数
        argv = sys.argv
        if len(argv) < 2:
            print('no port, eg. python2 index.py 9000')
            exit()

        host = argv[1]
        hosts = host.split(':')
        if len(hosts) == 2:
            host = hosts[0]
            port = hosts[1]
        else:
            host = '0.0.0.0'
            port = hosts[0]

        app = tornado.web.Application(route, **setting)
        # http_server = tornado.httpserver.HTTPServer(app, xheaders=True)
        # http_server.bind(port, host)
        # http_server.start(num_processes=0)
        app.listen(port, host)
        tornado.ioloop.IOLoop.instance().start()


# class error(Controller):
#   """ 错误处理
#   """
#
#   def index(self):
#       self.display('404', '../view')
