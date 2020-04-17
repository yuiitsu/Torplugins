# -*- coding:utf-8 -*-

"""
@author onlyfu
@time 2017/8/31
"""
import tornado.gen
from base.service import ServiceBase
from tools.verify import Verify


class Service(ServiceBase):
    buyer_model = None

    def __init__(self):
        """
        对象初始化方法
        添加你需要使用的model
        格式 项目model文件夹下的文件名或者 包名1.包名2.文件名 (无.py后缀)
        """
        self.buyer_model = self.import_model('buyer.model')

    @tornado.gen.coroutine
    def login_buyer(self, params):
        """
        买家web登录
        :param params:
        :return:
        """
        check_params = ['shop_id', 'account', 'password']
        if self.common_utils.is_empty(check_params, params):
            raise self._gre('PARAMS_NOT_EXIST')

        # 校验手机号是否合法
        account_type, is_valid = Verify.is_valid(params['account'])
        if not is_valid:
            raise self._gre('ACCOUNT_FORMAT_ERROR')

        # 查询买家信息
        buyer_data = yield self.buyer_model.query_buyer_by_account(params)
        if buyer_data is False:
            raise self._gre('SQL_EXECUTE_ERROR')
        elif buyer_data is None:
            raise self._gre('DATA_NOT_EXIST')

        # 检查密码
        encrypt_password = self.md5(self.md5(params['password']) + buyer_data['salt'])
        if encrypt_password != buyer_data['password']:
            raise self._gre('PASSWORD_ERROR')

        # 查询关联账号
        buyer_id_list = []
        bind_buyer_id = buyer_data['bind_buyer_id']
        if bind_buyer_id and bind_buyer_id != buyer_data['buyer_id']:
            buyer_id_list.append(bind_buyer_id)

            bind_buyer_info = yield self.buyer_model.query_bind_buyer(params['shop_id'], bind_buyer_id)
            if bind_buyer_info:
                buyer_id_list.extend([buyer['buyer_id'] for buyer in bind_buyer_info])
        else:
            buyer_id_list.append(buyer_data['buyer_id'])

        result = {
            'origin': buyer_data['origin'],
            'mobile': buyer_data['mobile'],
            'email': buyer_data['email'],
            'shop_id': buyer_data['shop_id'],
            'scene_type': buyer_data['scene_type'],
            'buyer_id': buyer_data['buyer_id'],
            'buyer_id_list': buyer_id_list,
            'account': buyer_data['account']
        }

        raise self._grs(result)

    @tornado.gen.coroutine
    def create_buyer(self, params):
        """
        创建买家
        """
        create_func_map = {
            1: 'create_from_app',
            2: 'create_from_wechat',
            3: 'create_from_web'
        }
        create_func_name = create_func_map.get(int(params['scen_type']), '')
        result = yield getattr(self, create_func_name)(params)

        raise self._gr(result)

    @tornado.gen.coroutine
    def create_from_app(self, params):
        pass

    @tornado.gen.coroutine
    def create_from_wechat(self, params):
        """
        微信登录中 scen_type 为 2 scen_id 为 app_id, buyer_id 为 open_id
        微信登录不需要密码和 salt, shop_id 暂定为 ‘wemart’
        """
        # 校验参数非空
        if self.common_utils.is_empty(['shop_id', 'buyer_id'], params):
            raise self._gre('PARAMS_NOT_EXIST')

        params['mobile'] = ''
        params.setdefault('origin', 'wechat')

        # 微信中scene_type为mini_app或wechat，scene_type原始数据为int常量，所以需要重新赋值
        params['scene_type'] = params['origin']
        params['password'] = ''
        params['salt'] = ''
        params['account'] = params['buyer_id']
        params['type'] = params['origin']
        params['scene_id'] = params['scen_id']
        params['bind_buyer_id'] = ''

        # 查询买家信息
        buyer_data = yield self.buyer_model.query_buyer_by_account(params)
        # 记录是否第一次注册
        is_new = 1
        if buyer_data is not None:
            is_new = 0
            # 如果为微信场景，则补足scene_id，修复scene_id
            yield self.buyer_model.update_buyer_account({
                'shop_id': params['shop_id'],
                'buyer_id': params['buyer_id'],
                'scene_id': params['scene_id'],
                'union_id': params.get('union_id', '')
            })

            # 账号如果存在，需要查询关联账号
            buyer_id_list = []
            bind_buyer_id = buyer_data['bind_buyer_id']
            if bind_buyer_id and bind_buyer_id != buyer_data['buyer_id']:
                buyer_id_list.append(bind_buyer_id)

                bind_buyer_info = yield self.buyer_model.query_bind_buyer(params['shop_id'], bind_buyer_id)
                if bind_buyer_info:
                    buyer_id_list.extend([buyer['buyer_id'] for buyer in bind_buyer_info])
            else:
                buyer_id_list.append(buyer_data['buyer_id'])

            buyer_data['buyer_id_list'] = buyer_id_list
            buyer_data['is_new'] = is_new
            raise self._grs(buyer_data)

        # 创建买家
        res = yield self.buyer_model.create_buyer(params)
        if res is None:
            raise self._gre('SQL_EXECUTE_ERROR')
        params['buyer_id_list'] = [params['buyer_id']]
        params['is_new'] = is_new
        raise self._grs(params)

    @tornado.gen.coroutine
    def create_from_web(self, params):
        """
        从WEB注册买家帐号
            Updated by Yuiitsu on 2018-01-08
        :param params:
            params['shop_id'] 店铺ID(*)
            params['mobile'] 手机号(*)
            params['password'] 密码(*)
            params['check_password'] 确认密码(*)
            params['verify_code'] 验证码(*)
        :return:
        """
        check_params = [
            'shop_id',
            'account',
            'password',
            'check_password',
            'verify_code'
        ]
        if self.common_utils.is_empty(check_params, params):
            raise self._gre('PARAMS_NOT_EXIST')

        # 校验 password ，re_password 一致
        if params['password'] != params['check_password']:
            raise self._gre('PASSWORD_NOT_MATCH')

        # 校验账号是否合法
        account_type, is_valid = Verify.is_valid(params['account'])
        if not is_valid:
            raise self._gre('ACCOUNT_FORMAT_ERROR')
        params[account_type] = params['account']
        params['type'] = account_type

        # 验证码处理
        code = yield self.redis.get(self.cache_key_predix.VERIFY_CODE + params['account'])
        if params['verify_code'].lower() != code:
            raise self._gre('VERIFY_CODE_ERROR')
        else:
            yield self.redis.delete(self.cache_key_predix.VERIFY_CODE + params['account'])

        # 查询买家信息
        buyer_data = yield self.buyer_model.query_buyer_by_account(params)
        if buyer_data is not None:
            raise self._gre('DATA_EXIST')

        # 创建买家
        salt = self.salt()
        request_password = params['password']
        password = self.md5(self.md5(request_password) + salt)
        params['password'] = password
        params['salt'] = salt
        params['buyer_id'] = self.create_uuid()
        params['scene_type'] = 'web'
        params['origin'] = 'web'

        res = yield self.buyer_model.create_buyer(params)
        if res is None:
            raise self._gre('SQL_EXECUTE_ERROR')

        params['password'] = request_password
        login_data = yield self.login_buyer(params)

        # 2018-11-13 delu 买家注册成功之后创建顾客
        yield self.load_extensions('after_buyer_register', {
            'shop_id': params['shop_id'],
            'buyer_id': params['buyer_id'],
            'email': params['account'],
            'scene_type': 'web',
            'sale_channel': '1',
            'create_time': '0000-00-00'
        })

        raise self._grs(login_data['data'])

    @tornado.gen.coroutine
    def bind_create_buyer(self, params):
        # 校验参数非空
        if self.common_utils.is_empty(['shop_id', 'scen_type', 'scen_id', 'mobile_no', 'password'], params):
            raise self._gre('PARAMS_NOT_EXIST')

        # 校验手机号是否合法
        if not Verify.ismobile(params['mobile_no']):
            raise self._gre('BUYER_PARAMS_FORMAT_ERROR')

        # 创建买家
        salt = self.salt()
        password = self.md5(self.md5(params['password']) + salt)
        params['password'] = password
        params['salt'] = salt

        params['buyer_id'] = 'B' + self.salt(32).upper()
        params['bind_buyer_id'] = params['buyer_id']

        # 其它
        params['other'] = ''

        # 调用 model
        res = yield self.buyer_model.create_buyer(params)

        if res is None:
            raise self._gre('SQL_EXECUTE_ERROR')
        else:
            result = self._e('SUCCESS')
            raise self._gr(result)

    @tornado.gen.coroutine
    def query_buyer_onlymobile(self, params):
        """
        查询买家信息
        :param params:
        :return:
        """
        # 调用 model
        buyer_data = yield self.buyer_model.query_buyer_by_mobile(params)
        raise self._gr(buyer_data)

    @tornado.gen.coroutine
    def logout(self, param):
        pass

    @tornado.gen.coroutine
    def bind_mobile(self, params):
        """
        绑定手机号
        :param params:
        :return:
        """
        # 调用 model
        buyer_data = yield self.buyer_model.bind_mobile(params)
        raise self._gr(buyer_data)

    @tornado.gen.coroutine
    def query_bind(self, params):
        """
        绑定手机号
        :param params:
        :return:
        """
        # 调用 model
        buyer_data = yield self.buyer_model.query_bind(params)
        raise self._gr(buyer_data)

    @tornado.gen.coroutine
    def update_buyer(self, params):
        """
        更新买家信息
        :param params: 
        :return: 
        """
        if self.common_utils.is_empty(['buyer_id', 'shop_id'], params):
            raise self._gre('PARAMS_NOT_EXIST')
        result = yield self.buyer_model.update_buyer(params)
        if not result:
            raise self._gre('SQL_EXECUTE_ERROR')
        raise self._grs()

    @tornado.gen.coroutine
    def query_buyer_list(self, params):
        """
        查询买家列表
        :param params: 
        :return: 
        """
        if self.common_utils.is_empty(['shop_id'], params):
            raise self._gre('PARAMS_NOT_EXIST')
        result = yield self.buyer_model.query_buyer_list(params)
        if result is False:
            raise self._gre('SQL_EXECUTE_ERROR')
        raise self._grs(result)

    @tornado.gen.coroutine
    def query_buyer_one(self, params):
        """
        查询单个买家
        :param params: 
        :return: 
        """
        if self.common_utils.is_empty(['buyer_id', 'shop_id'], params):
            raise self._gre('PARAMS_NOT_EXIST')
        result = yield self.buyer_model.query_buyer(params)
        if not result:
            raise self._gre('BUYER_NOT_FIND')
        raise self._grs(result)

    @tornado.gen.coroutine
    def query_buyer_by_account(self, params):
        """
        查询账号
        :param params:
        :return:
        """
        if self.common_utils.is_empty(['account', 'shop_id'], params):
            raise self._gre('PARAMS_NOT_EXIST')
        result = yield self.buyer_model.query_buyer_by_account(params)
        if not result:
            raise self._gre('BUYER_NOT_FIND')

        raise self._grs(result)

    @tornado.gen.coroutine
    def bind_buyer_account(self, params):
        """
        当前账号绑定其它账号
            当前账号绑定的账号没有绑定到其它账号: 当前账号绑定目标账号
            当前账号绑定的账号绑定过其它账号: 当前账号绑定目标账号的bind_account
            绑定成功后同时更新主账号用户信息(mobile/email)
        :param params:
            params['buyer_id']  当前用户id
            params['buyer_token']  当前用户buyer_token用于绑定成功后刷新用户信息
            params['shop_id']   当前用户所在店铺id
            params['account']   绑定到账号account
            params['verify_code']   绑定账号收到的验证码
        :return:

        """
        if self.common_utils.is_empty(['buyer_id', 'shop_id', 'account', 'verify_code'], params):
            raise self._gre('PARAMS_NOT_EXIST')

        # 查询被绑定账号信息
        bind_account = yield self.query_buyer_by_account(
            {
                'account': params['account'],
                'shop_id': params['shop_id']
            }
        )
        if bind_account['code'] != 0:
            # 创建买家主账号
            salt = self.salt()
            request_password = params['account']
            password = self.md5(self.md5(request_password) + salt)
            buyer_id = self.create_uuid()
            create_params = {
                'password': password,
                'salt': salt,
                'buyer_id': buyer_id,
                'scene_type': 'web',
                'origin': 'web',
                'account': params['account'],
                'shop_id': params['shop_id'],
                'type': params.get('type', 'mobile')
            }

            if create_params.get('type', 'mobile') == 'mobile' and Verify.ismobile(params['account']):
                create_params['mobile'] = create_params['account']

            res = yield self.buyer_model.create_buyer(create_params)

            if not res:
                raise self._gre('SQL_EXECUTE_ERROR')
            bind_account = {
                'data': {
                    'buyer_id': buyer_id,
                    'account': params['account'],
                    'bind_buyer_id': ''
                }
            }

        bind_account = bind_account['data']

        # 查询绑定账号是否绑定了其它账号
        if bind_account['bind_buyer_id']:
            bind_account = yield self.query_buyer_by_account(
                {
                    'buyer_id': bind_account['buyer_id'],
                    'account': bind_account['bind_buyer_id'],
                    'shop_id': bind_account['shop_id']
                }
            )
            if bind_account['code'] != 0:
                raise self._gr(bind_account)
            bind_account = bind_account['data']

        # 验证码处理
        # code = yield self.redis.get(self.cache_key_predix.VERIFY_CODE + params['account'])
        # if params['verify_code'].lower() != code:
        #     raise self._gre('VERIFY_CODE_ERROR')
        # else:
        #     yield self.redis.delete(self.cache_key_predix.VERIFY_CODE + params['account'])

        # 查询用户当前账号信息
        buyer_account = yield self.query_buyer_one({
            'buyer_id': params['buyer_id'],
            'shop_id': params['shop_id']
        })
        if buyer_account['code'] != 0:
            raise self._gr(buyer_account)
        buyer_account = buyer_account['data']

        # 绑定账号
        bind_params = {
            'buyer_id': bind_account['buyer_id'],
            'account': buyer_account['account'],
            'shop_id': params['shop_id'],
            'bind_buyer_id': bind_account['bind_buyer_id'] if bind_account['bind_buyer_id'] else bind_account['account'],
            'channel': params.get('channel', '')
        }
        if buyer_account['type'] == 'mobile':
            bind_params['mobile'] = buyer_account['account']
            bind_account['mobile'] = buyer_account['account']
        elif buyer_account['type'] == 'email':
            bind_params['email'] = buyer_account['account']
            bind_account['email'] = buyer_account['account']

        res = yield self.buyer_model.bind_buyer_account(bind_params)

        if res is None:
            raise self._gre('SQL_EXECUTE_ERROR')

        # 绑定手机时去更改对应顾客手机号
        if params.get('type', 'mobile') == 'mobile' and Verify.ismobile(params['account']):
            update_mobile = yield self.do_service(
                'crm.customer.service',
                'update_mobile',
                {
                    'shop_id': params['shop_id'],
                    'mobile': params['account'],
                    'buyer_id': params['buyer_id']
                }
            )
            if update_mobile['code'] != 0:
                raise self._gr(update_mobile)

        # todo: 刷新用户信息
        # 查询关联账号
        buyer_id_list = []
        bind_buyer_id = params['account']
        if bind_buyer_id and bind_buyer_id != params['buyer_id']:
            buyer_id_list.append(bind_buyer_id)

            bind_buyer_info = yield self.buyer_model.query_bind_buyer(params['shop_id'], bind_buyer_id)
            if bind_buyer_info:
                buyer_id_list.extend([buyer['buyer_id'] for buyer in bind_buyer_info])
        else:
            buyer_id_list.append(params['buyer_id'])

        result = {
            'origin': params['origin'],
            'mobile': params['mobile'],
            'email': params['email'],
            'shop_id': params['shop_id'],
            'scene_type': params['scene_type'],
            'buyer_id': params['buyer_id'],
            'buyer_id_list': buyer_id_list,
            'account': params['origin_account']
        }

        params['buyer_data'].update({
            'bind_buyer_id': params['account'],
            'buyer_id_list': buyer_id_list
        })

        raise self._grs(result)

    @tornado.gen.coroutine
    def query_main_account_list(self, params):
        """
        根据buyer_id_list, 查询绑定的主账号对应的用户信息(手机，邮箱都更新在这个用户上)
        :param params:
        :return:
        """
        if self.common_utils.is_empty(['buyer_id_list', 'shop_id'], params):
            raise self._gr('PARAMS_NOT_EXIST')
        res = yield self.buyer_model.query_main_account_list(params)
        if res is False:
            raise self._gre('SQL_EXECUTE_ERROR')
        # buyer_id_dict {主账号buyer_id: 当前buyer_id}
        buyer_id_dict = {}
        for account in res:
            buyer_id = account['buyer_id']
            main_account = account['a2.buyer_id'] if account['a2.buyer_id'] else buyer_id
            buyer_id_dict[main_account] = buyer_id

        new_buyer_id_list = params['buyer_id_list'].copy()
        new_buyer_id_list.extend(buyer_id_dict.keys())
        new_buyer_id_list = set(new_buyer_id_list)
        buyer_info_list = yield self.query_buyer_list({
            'buyer_id_list': new_buyer_id_list,
            'shop_id': params['shop_id']
        })
        if buyer_info_list['code'] != 0:
            raise self._gr(buyer_info_list)
        buyer_info_list = buyer_info_list['data']
        buyer_info_dict = {buyer['buyer_id']: buyer for buyer in buyer_info_list}

        buyer_res = []
        for buyer_id in params['buyer_id_list']:
            # 除了手机和邮箱都用原用户
            buyer_info = {
                'mobile': '',
                'email': '',
            }
            append_flag = 0
            for buyer_data in buyer_info_list:
                if buyer_data['buyer_id'] == buyer_id:
                    # 当前用户信息
                    append_flag = 1
                    buyer_data.pop('mobile', None)
                    buyer_data.pop('email', None)
                    buyer_info.update(buyer_data)
                elif buyer_id_dict.get(buyer_data['buyer_id']) == buyer_id:
                    if buyer_data.get('mobile'):
                        buyer_info['mobile'] = buyer_data['mobile']
                    if buyer_data.get('email'):
                        buyer_info['email'] = buyer_data['email']
            if append_flag == 1:
                buyer_res.append(buyer_info)

        raise self._grs(buyer_res)


if __name__ == '__main__':
    from tornado.ioloop import IOLoop


    @tornado.gen.coroutine
    def get_future():
        try:
            s = Service()
            # params = {
            #     'shop_id': '7',
            #     'buyer_id': 'oZ9XDv_YnYMlnq9inQvZKURFba-8',
            #     'account': '15800502039',
            #     'verify_code': '123456'
            # }
            # res = yield s.bind_buyer_account(params)

            params = {
                'shop_id': '139',
                'buyer_id_list': ['oZ9XDv_YnYMlnq9inQvZKURFba-8', 'd29bbdcdd75807a19759463102d2aea5']
            }
            res = yield s.query_main_account_list(params)

            print('*' * 100)
            print(s.json.dumps(res, ensure_ascii=False, cls=s.date_encoder))
            print('*' * 100)
        except Exception as e:
            print(e)
        finally:
            IOLoop.current().stop()


    get_future()

    IOLoop.current().start()