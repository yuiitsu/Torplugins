# -*- coding:utf-8 -*-

import datetime
import hashlib
import importlib
import json
import random
import time

import tornado.escape
import tornado.gen

import conf.config as config
from constants.cachekey_predix import CacheKeyPredix
from constants.constants import Constants
from constants.error_code import Code
from source.properties import Properties
from source.redisbase import RedisBase
from source.async_redis import AsyncRedis
from source.service_manager import ServiceManager as serviceManager
from tools.common_util import CommonUtil
from tools.date_json_encoder import CJsonEncoder
from tools.date_utils import DateUtils
from tools.excel_util import excel_util
from tools.httputils import HttpUtils
from tools.rsa_utils import RsaUtils
from tools.logs import Logs
from tools.string_util import StringUtils


class ServiceBase(object):
    dicConfig = config.CONF
    time = time
    datetime = datetime
    json = json
    hashlib = hashlib
    constants = Constants
    error_code = Code
    cache_key_predix = CacheKeyPredix
    properties = Properties()
    # redis = AsyncRedis()
    redis = RedisBase()
    httputils = HttpUtils
    date_utils = DateUtils
    common_utils = CommonUtil
    string_utils = StringUtils
    date_encoder = CJsonEncoder
    rsa_utils = RsaUtils
    excel_util = excel_util
    logger = Logs().logger
    language_code = {}

    # tornado_redis = TornadoRedis()

    def md5(self, text):
        """
        md5加密
        :param text: 
        :return: 
        """
        result = hashlib.md5(text)
        return result.hexdigest()

    def import_model(self, model_name):
        """
        加载数据类
        :param model_name: string 数据类名
        :return: 
        """
        try:
            model = importlib.import_module('module.' + model_name)
            return model.Model()
        except Exception, e:
            print e
            return None

    def time_to_mktime(self, time_str, format_str):
        """
        将时间字符串转化成时间戳
        :param params: 
        :return: 
        """
        return time.mktime(time.strptime(time_str, format_str))

    def salt(self, salt_len=6, is_num=False):
        """ 
        密码加密字符串
        生成一个固定位数的随机字符串，包含0-9a-z
        @:param salt_len 生成字符串长度
        """

        if is_num:
            chrset = '0123456789'
        else:
            chrset = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWSYZ'
        salt = []
        for i in range(salt_len):
            item = random.choice(chrset)
            salt.append(item)

        return ''.join(salt)

    def create_uuid(self):
        """
        创建随机字符串
        :return: 
        """
        m = hashlib.md5()
        m.update(bytes(str(time.time()) + self.salt(12)))
        return m.hexdigest()

    def loads_list(self, list_str):
        """
        转换字符串成列表
        :param list_str: 
        :return: 
        create:wsy 2017/7/31
        """
        try:
            data_list = self.json.loads(list_str)
        except Exception, e:
            print e
            data_list = []
        return data_list

    def loads_dic(self, dic_str):
        """
        转换字符串成字典
        :param dic_str: 
        :return: 
        create:wsy 2017/7/31
        """
        try:
            data_dic = self.json.loads(dic_str)
        except Exception, e:
            print e
            data_dic = {}
        return data_dic

    def escape_string(self, data, un=None):
        """
        特殊字符转义
        :param data: string, tuple, list, dict 转义数据
        :param un: 
        :return: 
        """
        if isinstance(data, str):
            return tornado.escape.xhtml_escape(data) if not un else tornado.escape.xhtml_unescape(data)
        elif isinstance(data, tuple) or isinstance(data, list):
            lisData = []
            for item in data:
                lisData.append(
                    tornado.escape.xhtml_escape(str(item)) if not un else tornado.escape.xhtml_unescape(str(item)))

            return lisData
        elif isinstance(data, dict):
            for key in data:
                data[key] = tornado.escape.xhtml_escape(str(data[key])) if not un else tornado.escape.xhtml_unescape(
                    str(data[key]))

            return data

    def do_service(self, service_path, method, params={}):
        """
        调用服务
        :param service_path: 
        :param method: 
        :param params: 
        :return: 
        """
        return serviceManager.do_service(service_path, method, params=params, version=config.CONF['version'])

    def sign_params(self, params, secret_key):
        """
        验签
        :param params:
        :param secret_key:
        :return:
        """

        params_keys = []
        for (k, v) in params.items():
            if k != 'sign':
                params_keys.append(k)

        params_string = ''
        for key in sorted(params_keys):
            params_string += (key + '=' + params[key] + '&')
        params_string = self.md5(params_string + secret_key).upper()
        return cmp(params_string, params['sign'].upper())

    @tornado.gen.coroutine
    def load_extensions(self, trigger_position, data):
        """
        加载扩展程序
        :param trigger_position:
        :param data:
        :return:
        """
        result = yield self.do_service('cfg.extensions.service', 'query', {'trigger_position': trigger_position})
        if result and 'code' in result and result['code'] == 0:
            # 发送消息
            for item in result['data']:
                service_path = item['package_path']
                method = item['method']
                self.publish_message(service_path, method, data)

    def publish_message(self, service_path, method, params, task_key=None):
        """
        发消息到队列中心(redis)
        :return: 
        """
        self.logger.info('发消息 service: %s, method: %s, params: %s', service_path, method,
                         self.json.dumps(params, cls=self.date_encoder))
        try:
            if task_key is None:
                task_key = self.cache_key_predix.TASK_DATA_LIST
            result = self.redis.lpush(task_key, self.json.dumps({
                'service_path': service_path,
                'method': method,
                'params': params
            }, cls=self.date_encoder))
            return result
        except Exception, e:
            self.logger.error(e.message)
            return False

    def web_event(self, method, event_list, request, data, agent_status=''):
        """
        页面事件
        :param method:
        :param event_list:
        :param request:
        :param data:
        :param agent_status: 用于判断，是否要记录用户的访问信息，便于后面获取不到用户访问信息时使用，如支付回调
        :return:
        """
        t = time.time()
        cache_key = 'buyer:agent:' + agent_status
        if not request:
            request_str = self.redis.get(cache_key)
            request = self.json.loads(request_str)
        else:
            request_str = self.json.dumps(request)
            if agent_status:
                self.redis.set_value(cache_key, request_str)

        self.logger.warning('web_event request: %s, data: %s , time: %s', request_str, self.json.dumps(data), t)
        message_data = {
            'event_list': event_list,
            'request': request,
            'data': data,
            'time': t
        }
        print message_data
        return self.publish_message('task.statistics.sa.service', method, message_data)

    def _e(self, error_key):
        """
        :param error_key: 
        :return: 
        """
        data = {}
        for key in self.error_code[error_key]:
            data[key] = self.error_code[error_key][key]
        if error_key in self.language_code:
            data['msg'] = self.language_code[error_key]

        return data

    def _gre(self, data):
        """
        tornado.gen.Return
        :param data: 数据
        :return: 
        """
        return tornado.gen.Return(self._e(data))

    def _grs(self, data={}):
        """
        成功返回
        :param data: 
        :return: 
        """
        result = self._e('SUCCESS')
        result['data'] = data
        return tornado.gen.Return(result)

    def _gr(self, data):
        """
        tornado.gen.Return
        :param data: 数据
        :return: 
        """
        return tornado.gen.Return(data)

    def cache_get(self, key):
        result = self.redis.get(key)
        if result:
            expire = self.redis.ttl(key)
            if expire < self.properties.get('expire', 'CACHE_REFRESH_EXPIRE'):
                self.redis.expire(key, self.properties.get('expire', 'CACHE_EXPIRE'))
            try:
                result = json.loads(result)
            except Exception as e:
                self.redis.expire(key, 0)
                result = False
            return result
        else:
            return False

    def cache_set(self, key, value):
        try:
            value = json.dumps(value, cls=self.date_encoder)
            self.redis.set(key, value)
            self.redis.expire(key, self.properties.get('expire', 'CACHE_EXPIRE'))
        except Exception:
            return


if __name__ == '__main__':
    service = ServiceBase()
    # params = {
    #     'goods_id': 'G00JL1GTCZ',
    #     'sku_id': 'S00QAJ1LPP',
    #     'update_stock': -1,
    #     'update_sale': 1,
    # }
    # service.publish_message('task.stock_service', 'upadte_stock_sale', params)
    a = '[{"comp_id":6,"comp_content":{"module1":{"btnLinkIsSame":true,"imgUrl":"http://7fvdme.com1.z0.glb.clouddn.com/dfa1da5c-5f43-7916-ae72-83a4d00c","btnBgColor":"#3DA2E0","content":"标 题"},"module2":{"btnLinkIsSame":true,"imgUrl":"http://7fvdme.com1.z0.glb.clouddn.com/3aeb7e89-e76a-7d4e-3b7a-f33b7e30","content":"标题"},"module3":{"btnLinkIsSame":true,"imgUrl":"http://7fvdme.com1.z0.glb.clouddn.com/ad37b676-097d-f073-d591-3d9d2b21","content":"标题"},"margin":"4.284"},"comp_type":5,"comp_name":"mosaic_1","create_time":"1497431841","comp_key":"mosaic_1","theme_id":0,"page_id":0,"comp_image":"http://imgcache1.qiniudn.com/6c69bb49-caf0-71d8-8a82-9d341e9b?imageView2/2/w/144/h/144","componentKey":"component7de3d71b-629f-488c-0ba1-cd42f199e3c4"},{"comp_id":31,"comp_content":{"module":[{"coupon":{"activity_id":15,"activity_name":"优惠券1","goods_discount":1,"goods_money":0}},{"coupon":{"activity_id":17,"activity_name":"优惠券3","goods_discount":3,"goods_money":222}},{"coupon":{"activity_id":17,"activity_name":"优惠券3","goods_discount":3,"goods_money":222}}],"length":3,"active":1,"margin":"4.284"},"comp_type":11,"comp_name":"coupon_1","create_time":"1499926689","comp_key":"coupon_1","theme_id":0,"page_id":0,"comp_image":"","componentKey":"component17feba7e-7aa6-cff3-5ee3-b10da2afe6a2"},{"comp_id":22,"comp_content":{"margin":"4.284","module":[{"imgUrl":"http://imgcache1.qiniudn.com/eecb3259-7f26-ac18-020a-9466c331","title":"副标题","content":"标题","link":{"page_id":98,"shop_id":"16","url":"shelf?shop_id=16&page_id=98","name":"商城"}},{"imgUrl":"http://7fvdme.com1.z0.glb.clouddn.com/dfa1da5c-5f43-7916-ae72-83a4d00c","title":"副标题","content":"标题"}],"cardStyle":"1","num":"2","bgColor":"#fff","position":"center center","length":2,"active":0},"comp_type":5,"comp_name":"mosaic_3","create_time":"1497439435","comp_key":"mosaic_3","theme_id":0,"page_id":0,"comp_image":"http://imgcache1.qiniudn.com/4b067eff-bbb8-6eea-7a10-11a4723e?imageView2/2/w/144/h/144","componentKey":"component666489b4-f8ee-f'
    b = '[{"comp_id":2,"comp_content":{},"comp_type":1,"comp_name":"header_1","create_time":"1497431840","comp_key":"header_1","theme_id":0,"page_id":0,"componentKey":"componentfb7ccc53-ad00-651e-6a7e-68a8aa0d7d59"},{"comp_id":20,"comp_content":{"module":[{"imgUrl":"http://7fvdme.com1.z0.glb.clouddn.com/00c7e3d7-034a-dd8b-00e7-bc9bd9f9","link":{"goods_id":"G00RIIKD1S","shop_id":"7","url":"product?shop_id=7&id=G00RIIKD1S","name":"Nike耐克官方 NIKE LUNAREPIC LOW FLYKNIT 2女子跑步运动 863780"},"action_1":"立即购买","text":" ","title":" "},{"imgUrl":"http://7fvdme.com1.z0.glb.clouddn.com/76f0debc-5ca7-465e-b534-26169ef2","text-color":"rgb(21, 137, 238)","action_1":"了解更多","action_1-color":"rgb(21, 137, 238)","text":" ","title":" ","title-color":"rgb(21, 137, 238)","link":{"goods_id":"G00TVJQTNJ","shop_id":"7","url":"product?shop_id=7&id=G00TVJQTNJ","name":"Nike 耐克官方 NIKE TANJUN 男子运动休闲鞋 812654"}},{"imgUrl":"http://7fvdme.com1.z0.glb.clouddn.com/960636bc-4a08-1a1f-aa14-f090e327","title":" ","text":"跑步无极限","action_1":"了解更多","link":{"page_id":105,"shop_id":"7","url":"shelf?shop_id=7&page_id=105","name":"商城"}}],"timeout":"5","length":3,"active":1,"position":"center center","margin":"0","overlay":"0","auto":true,"type":"slider"},"comp_type":4,"comp_name":"hero_image_slider_1","create_time":"1497439435","comp_key":"hero_image_slider_1","theme_id":0,"page_id":0,"componentKey":"componentfedb2efa-8fad-8453-a199-2a8de6dca6bb"},{"comp_id":28,"comp_content":{"module1":{"content":"商品","link":{"page_id":105,"shop_id":"7","url":"shelf?shop_id=7&page_id=105","name":"商城"}},"module2":{"content":"销量排名","link":{"page_id":104,"shop_id":"7","url":"shelf?shop_id=7&page_id=104","name":"品牌故事"}},"module3":{"content":"优惠折扣","link":{"goods_id":"G00RIIKD1S","shop_id":"7","url":"product?shop_id=7&id=G00RIIKD1S","name":"Nike耐克官方 NIKE LUNAREPIC LOW FLYKNIT 2女子跑步运动 863780"}},"margin":"5.712","bgColor":"#E1E1E6"},"comp_type":3,"comp_name":"banner_2","create_time":"1498042651","comp_key":"banner_2","theme_id":0,"page_id":0,"componentKey":"component1b59aeb7-74da-f86e-d51d-1f45a91cc39b"},{"comp_id":6,"comp_content":{"module1":{"btnLinkIsSame":true,"link":{"goods_id":"G00QYYYFMA","shop_id":"7","url":"product?shop_id=7&id=G00QYYYFMA","name":"Nike 耐克官方 NIKE MAMBA INSTINCT EP 科比男子篮球运动鞋 8844"},"btnLink":{"goods_id":"G00QYYYFMA","shop_id":"7","url":"product?shop_id=7&id=G00QYYYFMA","name":"Nike 耐克官方 NIKE MAMBA INSTINCT EP 科比男子篮球运动鞋 8844"},"imgUrl":"http://7fvdme.com1.z0.glb.clouddn.com/dc834a74-69ec-b798-1205-bf1ef9c5","btnBgColor":"#EB5745","showBtn":true,"content":"NIKE","btnContext":"立即购买","hasBind":true},"module2":{"btnLinkIsSame":true,"imgUrl":"http://7fvdme.com1.z0.glb.clouddn.com/e2f3326d-7d88-98e6-34e4-3d91b2b7","content":"NIKE AIR","showBtn":true,"link":{"goods_id":"G00TVJQTNJ","shop_id":"7","url":"product?shop_id=7&id=G00TVJQTNJ","name":"Nike 耐克官方 NIKE TANJUN 男子运动休闲鞋 812654"},"btnLink":{"goods_id":"G00TVJQTNJ","shop_id":"7","url":"product?shop_id=7&id=G00TVJQTNJ","name":"Nike 耐克官方 NIKE TANJUN 男子运动休闲鞋 812654"},"hasBind":true,"btnContext":"BUY"},"module3":{"btnLinkIsSame":true,"imgUrl":"http://7fvdme.com1.z0.glb.clouddn.com/83dd8c7c-1aeb-9799-9220-85fb8f00","content":"AIR JORDAN I","link":{"goods_id":"G00QYYYFMA","shop_id":"7","url":"product?shop_id=7&id=G00QYYYFMA","name":"Nike 耐克官方 NIKE MAMBA INSTINCT EP 科比男子篮球运动鞋 8844"},"btnLink":{"goods_id":"G00QYYYFMA","shop_id":"7","url":"product?shop_id=7&id=G00QYYYFMA","name":"Nike 耐克官方 NIKE MAMBA INSTINCT EP 科比男子篮球运动鞋 8844"},"showBtn":true,"hasBind":true,"content-color":"rgb(255, 255, 255)"}},"comp_type":5,"comp_name":"mosaic_1","create_time":"1497431841","comp_key":"mosaic_1","theme_id":0,"page_id":0,"componentKey":"componentad7ca163-b1b9-77d3-2eaf-630d39c661a9"},{"comp_id":22,"comp_content":{"module":[{"link":{"page_id":134,"shop_id":"7","url":"shelf?shop_id=7&page_id=134","name":"足球世界"},"imgUrl":"http://7fvdme.com1.z0.glb.clouddn.com/c35a693e-0b82-c165-8ddb-aff513ce","title":"NIKE夏日休闲系列","content":"袜子鞋精选"}],"active":0,"position":"center center","bgColor":"#E1E1E6","margin":"4.284","length":1},"comp_type":5,"comp_name":"mosaic_3","create_time":"1497439435","comp_key":"mosaic_3","theme_id":0,"page_id":0,"componentKey":"component039b04ae-233b-82aa-621f-be0d916a3bf0"},{"comp_id":22,"comp_content":{"margin":"4.284","module":[{"imgUrl":"http://7fvdme.com1.z0.glb.clouddn.com/6d0e4757-d17a-9d32-8f27-d9092bda","title":"GO SKATEBOARDING DAY","content":"滑翻每一天"},{"imgUrl":"http://7fvdme.com1.z0.glb.clouddn.com/16f2c337-db59-7697-4411-32a57170","title":"夏日列练 秀出你的身材","content":"练不如炼"},{"imgUrl":"http://7fvdme.com1.z0.glb.clouddn.com/28063bc2-269a-02d5-401f-d45023ab","title":"非凡舒适体验和灵活支撑效果","content":"JORAN ULTRA.FLY 2"}],"cardStyle":"1","num":"2","bgColor":"#fff","position":"center center","active":2},"comp_type":5,"comp_name":"mosaic_3","create_time":"1497439435","comp_key":"mosaic_3","theme_id":0,"page_id":0,"componentKey":"componentc8efba38-3e97-68bd-a076-15939f5fb7f5"},{"comp_id":5,"comp_content":{"module":[{"imgUrl":"http://7fvdme.com1.z0.glb.clouddn.com/7ac31309-aa9e-0fb4-ec14-7a253743","title":"NEW ARRIVAL","text":"新品预览","action_1":"现在选购","link":{"page_id":134,"shop_id":"7","url":"shelf?shop_id=7&page_id=134","name":"足球世界"}}],"margin":"4.284","overlay":"4.284","position":"top center","title":"足球天堂","active":0},"comp_type":4,"comp_name":"hero_image_1","create_time":"1497431841","comp_key":"hero_image_1","theme_id":0,"page_id":0,"componentKey":"componentd2506737-6b72-93b7-81e5-64268e7e215c"},{"comp_id":8,"comp_content":{"margin":"2.856","column_num":"3","group_num":"","bgColor":"#fff","row_num":"2"},"comp_type":7,"comp_name":"product_grid_1","create_time":"1497431841","comp_key":"product_grid_1","theme_id":0,"page_id":0,"componentKey":"component28e3a10e-1296-8fa8-aa57-d949084d78af"},{"comp_id":3,"comp_content":{"company":"© 2017. &nbsp;微猫版权所有","module1":{},"module2":{},"module3":{},"margin":"5.712"},"comp_type":2,"comp_name":"footer_1","create_time":"1497431840","comp_key":"footer_1","theme_id":0,"page_id":0,"componentKey":"componentbe03b69f-423d-a2c1-9825-daa9df530402"}]'
    print len(b)
    print service.time_to_mktime('2017-7-18 12:32:34', '%Y-%m-%d %H:%M:%S')
