# -*- coding:utf-8 -*-

"""
@author: delu
@file: error_code.py
@time: 17/4/19 下午3:10
"""

Code = {
    # 1 通用
    'SUCCESS': {'code': 0, 'msg': '成功'},
    'REQUEST_TYPE_ERROR': {'code': 1001, 'msg': '请求类型错误'},
    'SQL_EXECUTE_ERROR': {'code': 1002, 'msg': '数据库执行失败'},
    'CACHE_EXECUTE_ERROR': {'code': 1003, 'msg': '缓存执行失败'},
    'PARAMS_NOT_EXIST': {'code': 1004, 'msg': '参数错误'},
    'PARAMS_TYPE_ERROR': {'code': 1005, 'msg': '参数类型错误'},
    'AUTH_ERROR': {'code': 1006, 'msg': '用户无权限'},
    'NOT_LOGIN': {'code': 1007, 'msg': '用户未登录'},
    'DATA_EXIST': {'code': 1008, 'msg': '数据已存在'},
    'DATA_NOT_EXIST': {'code': 1008, 'msg': '数据不存在'},
    'PARAMS_DATE_ERROR': {'code': 1009, 'msg': '时间类型错误'},
    'JSON_DATA_FORMAT_ERROR': {'code': 1010, 'msg': 'JSON数据格式错误'},
    'AMOUNT_TYPE_ERROR': {'code': 1011, 'msg': '金额类型错误'},
    'EMAIL_SEND_ERROR': {'code': 1012, 'msg': '邮件发送失败'},
    'AUTH_SET_ERROR': {'code': 1013, 'msg': '权限设置错误'},
    'SIGN_VERIFY_FAILED': {'code': 1014, 'msg': '验签失败'},
    'HTTP_REQUEST_FAILED': {'code': 1015, 'msg': 'HTTP请求失败'},

    # 2 用户模块
    # 密码相关
    'PASSWORD_ERROR': {'code': 2101, 'msg': '账号密码不匹配'},
    'PASSWORD_NOT_MATCH': {'code': 2102, 'msg': '两次密码不匹配'},
    #
    'ACCOUNT_CREATE_FAILED': {'code': 2009, 'msg': '账号创建失败'},
    'ADMIN_GROUP_ERROR': {'code': 2010, 'msg': '未查询到店铺的管理员分组'},
    'ADMIN_GROUP_ID_MISSING': {'code': 2011, 'msg': '该管理员分组不属于本店铺'},
    'ADMIN_ID_MISSION': {'code': 2012, 'msg': '该管理员不属于本店铺'},
    'ADMIN_MISSING': {'code': 2013, 'msg': '未查询到该店铺的管理员信息'},
    'ADMIN_STATUS_ERROR': {'code': 2014, 'msg': '管理员更新状态有误'},
    'ADMIN_SUPER_GROUP_ERROR': {'code': 2015, 'msg': '超级管理员不允许修改分组'},
    'ADMIN_CHANGE_STATUS_ERROR': {'code': 2016, 'msg': '管理员不能冻结自己'},
    'ACCOUNT_FREEZE': {'code': 2017, 'msg': '帐号被冻结'},

    # 3 店铺
    'SHOP_NOT_PERMISSION': {'code': 3003, 'msg': '你无权管理该店铺'},
    'SHOP_NOT_EXIST': {'code': 3007, 'msg': '店铺不存在'},
    'SHOP_DATA_ERROR': {'code': 3008, 'msg': '店铺数据异常'},

    # 4 买家模块
    'BUYER_PARAMS_FORMAT_ERROR': {'code': 4003, 'msg': '参数格式错误'},
    'BUYER_ACCOUNT_CREATE_ERROR': {'code': 4004, 'msg': '创建买家失败'},
    'BUYER_ACCOUNT_NOT_FOUND': {'code': 4006, 'msg': '买家帐号未找到'},
    'BUYER_SIGN_FAILURE': {'code': 4008, 'msg': '参数签名验证失败'},
    'SHOPPING_CART_PARAMS_NOT_EXIST': {'code': 4009, 'msg': '购物车参数非空'},
    'SHOPPING_CART_NOT_FIND': {'code': 4010, 'msg': '购物车未找到'},
    'SHOPPING_CART_BUYER_NOT_PERMISSION': {'code': 4011, 'msg': '买家无法操作该购物车'},
    'ADDRESS_CREATE_PARAMS_NOT_EXIST': {'code': 4012, 'msg': '创建买家收获地址，参数非空'},
    'ADDRESS_UPDATE_PARAMS_NOT_EXIST': {'code': 4013, 'msg': '更新买家收货地址, 参数非空'},
    'ID_CARD_QUERY_PARAMS_NOT_EXIST': {'code': 4014, 'msg': '查询买家身份证列表，参数非空'},
    'ID_CARD_UPDATE_PARAMS_NOT_EXIST': {'code': 4015, 'msg': '更新买家身份证列表，参数非空'},
    'ID_CARD_DELETE_PARAMS_NOT_EXIST': {'code': 4016, 'msg': '删除买家身份证列表，参数非空'},
    'BUYER_INVOICE_PARAMS_NULL': {'code': 4017, 'msg': '发票参数非空'},
    'BUYER_INVOICE_EXECUTE_FAIL': {'code': 4018, 'msg': '发票操作失败'},
    'BUYER_COLLECTION_PARAMS_NULL': {'code': 4019, 'msg': '买家收藏参数非空'},
    'BUYER_COLLECTION_EXECUTE_ERROR': {'code': 4019, 'msg': '买家收藏执行失败'},
    'ID_CARD_NAME_NOT_MATCH': {'code': 4020, 'msg': '身份证姓名和身份证号不匹配'},
    'ID_CARD_EXIST': {'code': 4021, 'msg': '身份证信息已存在'},
    'SHOPPING_CART_BUY_VOL_EMPTY': {'code': 4022, 'msg': '购买数量不能为0'},
    'BUYER_ALREADY_BIND': {'code': 4023, 'msg': '买家已经绑定'},
    'BUYER_BIND_ERROR': {'code': 4024, 'msg': '此帐号不能绑定'},
    'ID_CARD_ERROR': {'code': 4025, 'msg': '身份证校验错误'},

    # 4.1 收货地址
    'ADDRESS_DATA_NOT_FOUND': {'code': 4101, 'msg': '收货地址未找到'},
    'ADDRESS_DATA_NOT_MATCH': {'code': 4102, 'msg': '省市区数据不匹配'},

    # 5 商品模块
    'GOODS_PARAMS_ERROR': {'code': 5001, 'msg': '商品ID格式错误'},
    'GOODS_NOT_FIND': {'code': 5002, 'msg': '商品未找到'},
    'GOODS_NOT_BUY_SHOP_NOT_PERMISSION': {'code': 5003, 'msg': '商品不可购买，商品不属于当前店铺'},
    'GOODS_BUY_NOT_PERMISSION':
        {'code': 5004, 'msg': '商品不可购买(商品下架,商品金额为0,库存为0,商品金额发生了变动,购买数量超过了库存)'},
    'GOODS_OFF_SHELF': {'code': 5005, 'msg': '商品已下架'},
    'GOODS_MUST_OFF_SHELF': {'code': 5006, 'msg': '商品必须为下架状态才可编辑'},
    'GOODS_SHOP_NOT_PERMISSION': {'code': 5007, 'msg': '当前登录着无法编辑该商品'},
    'GOODS_PRICE_ERROR': {'code': 5008, 'msg': '商品价格错误'},
    # 5.1 sku
    'GOODS_SKU_ERROR': {'code': 5101, 'msg': '商品sku错误'},
    'GOODS_SKU_NOT_FOUND': {'code': 5102, 'msg': '未找到sku'},
    'GOODS_SKU_NOT_MATCH': {'code': 5103, 'msg': 'goods_id 与 sku_id不匹配'},
    'GOODS_SKU_JSON_ERROR': {'code': 5104, 'msg': 'sku json格式错误'},
    'GOODS_SKU_BUY_VOL_ERROR': {'code': 5105, 'msg': '购买数为0'},
    'GOODS_SKU_STOCK_NOT_ENOUGH': {'code': 5106, 'msg': '库存不足'},
    'GOODS_PROPERTIES_NAME_REPEAT': {'code': 5107, 'msg': '属性重复'},
    # 5.2 商品分组
    'GOODS_GROUP_NOT_FIND': {'code': 5201, 'msg': '商品分组未找到'},
    'GOODS_GROUP_AUTH_ERROR': {'code': 5202, 'msg': '商品参数错误，无操作该商品权限'},
    'GOODS_GROUP_VERIFY_WRONG': {'code': 5203, 'msg': '分组校验失败'},
    # 5.3 商品品牌
    # 5.4 商品标签
    'GOODS_TAGS_NOT_FOUND': {'code': 5401, 'msg': '未找到该商品标签'},
    # 5.5 商品分类
    'SUBCATEGORY_EXIST': {'code': 5501, 'msg': '该分类存在子分类，请先删除子分类'},

    # 6 订单模块
    'ORDER_CONFIRM_SKU_ERROR': {'code': 6001, 'msg': '订单确认失败，商品信息有误'},
    'ORDER_RECEIVE_NOT_EXIST':
        {'code': 6002, 'msg': '收货信息不完善(收货人姓名,收货人地址,收获人手机号,城市编号,身份证号)'},
    'ORDER_GOODS_DECREASE_STOCK_ERROR': {'code': 6003, 'msg': '扣商品库存失败'},
    'ORDER_STATUS_ERROR': {'code': 6004, 'msg': '订单状态已改变'},
    'ORDER_ADDRESS_CREATE_PARAMS_ERROR': {'code': 6005, 'msg': '订单order_id为空'},
    'ORDER_BUYER_NOT_PERMISSION': {'code': 6006, 'msg': '该买家无权操作当前订单'},
    'ORDER_SEND_PARAMS_NOT_EXIST': {'code': 6007, 'msg': '订单发货关键参数缺失(订单号,物流公司,物流单号)'},
    'ORDER_SHOP_NOT_PERMISSION': {'code': 6008, 'msg': '该商家无法操作当前订单'},
    'ORDER_RECEIVE_PARAMS_NOT_EXIST': {'code': 6009, 'msg': '订单收货关键参数缺失'},
    'ORDER_STATUS_CHANGE_NOT_PERMISSION': {'code': 6010, 'msg': '订单状态无法更改'},
    'ORDER_FARE_MONEY_ERROR': {'code': 6011, 'msg': '计算运费失败'},
    'ORDER_ORDER_SKU_NOT_MATCH': {'code': 6014, 'msg': '订单号和sku_id不匹配'},
    'ORDER_QUERY_ERROR': {'code': 6016, 'msg': '订单查询失败'},
    'ORDER_SKU_NOT_FIND': {'code': 6018, 'msg': '订单sku未找到'},
    'ORDER_DEPART_PARAMS_NOT_EXIST': {'code': 6021, 'msg': '拆单，参数非空'},
    'ORDER_DEPART_WAREHOUSE_PARAMS_NOT_EXIST': {'code': 6022, 'msg': '根据仓库进行拆单，参数非空'},
    'ORDER_COUNT_PARAMS_NOT_EXIST': {'code': 6023, 'msg': '统计订单数量，参数非空'},
    'ORDER_NOT_FIND': {'code': 6025, 'msg': '订单未找到'},
    'ORDER_CANCEL_ERROR': {'code': 6026, 'msg': '订单无法取消'},
    'ORDER_CONFIRM_ERROR': {'code': 6027, 'msg': '订单检查失败'},
    'ORDER_SEND_INSERT_FAIL': {'code': 6031, 'msg': '订单发货信息插入失败'},
    'ORDER_DATA_ERROR': {'code': 6032, 'msg': '订单数据异常'},
    'ORDER_ID_NOT_MATCH_SKU_ID': {'code': 6033, 'msg': '订单号和SKU不配置'},
    # 6.1 售后
    'REFUND_DATA_NOT_FOUND': {'code': 6101, 'msg': '售后申请数据未找到'},
    'REFUND_DATA_ERROR': {'code': 6102, 'msg': '售后申请数据异常'},
    'REFUND_STATUS_CHANGE': {'code': 6103, 'msg': '售后申请状态已改变'},
    'REFUND_APPROVE_MONEY_MORE': {'code': 6104, 'msg': '审核退款金额超过订单允许最大退款金额'},
    'REFUND_REQUEST_FAILED': {'code': 6105, 'msg': '退款请求失败'},
    'REFUND_REQUEST_FAILED_AND_SQL_ERROR': {'code': 6106, 'msg': '退款请求失败且数据库执行失败'},
    'REFUND_REQUEST_SUCCESS_BUT_SQL_ERROR': {'code': 6107, 'msg': '退款成功，但数据库执行失败'},
    'REFUND_APPLY_DATA_EXIST': {'code': 6108, 'msg': '申请数据已存在，且在进行中'},
    'REFUND_DATA_EXIST': {'code': 6109, 'msg': '有售后申请，无法执行该操作'},

    # 7 支付
    'PAY_PARAMS_NOT_ERROR': {'code': '7001', 'msg': '支付关键参数不存在'},
    'PAY_NOTIFY_XML_ERROR': {'code': '7002', 'msg': 'xml数据格式错误'},
    'PAY_PREPAY_ID_ERROR': {'code': '7003', 'msg': '获取预支付数据失败'},
    'PAY_TYPE_NOT_EXIST': {'code': 7004, 'msg': '支付类型不存在'},
    'PAY_SIGN_ERROR': {'code': 7005, 'msg': '支付宝验签失败'},
    'PAY_NOT_FIND': {'code': 7006, 'msg': '支付记录不存在'},
    'PAY_CREATE_PARAMS_NOT_EXIST': {'code': 7007, 'msg': '创建支付请求，参数非空'},
    'PAY_PAY_PARAMS_NOT_EXIST': {'code': 7008, 'msg': '支付请求参数不存在'},
    'PAY_REFUND_PARAMS_NOT_EXIST': {'code': 7009, 'msg': '退款请求参数不存在'},
    'PAY_REFUND_AMOUNT_ERROR': {'code': 7010, 'msg': '退款金额错误'},
    'PAY_REFUND_THIRD_SERVER_ERROR': {'code': 7011, 'msg': '第三方服务器异常'},
    'PAY_REFUND_REQUEST_ERROR': {'code': 7012, 'msg': '退款请求被拒绝'},
    'PAY_DATA_ERROR': {'code': 7013, 'msg': '支付数据异常'},

    # 9 微信小程序获取 sessionkey失败
    'MINI_APP_GET_SESSIONKEY_ERROR': {'code': 9003, 'msg': '微信小程序获取sessionkey失败'},
    'MINI_APP_FORM_ID_NOT_EXIST': {'code': 9004, 'msg': 'form_id和goods_id非空'},
    'MINI_APP_ACTIVITY_GOODS_ID': {'code': 9005, 'msg': 'goods_id和start_time非空'},
    'MINI_APP_APPID_ERROR': {'code': 9006, 'msg': '小程序appid错误'},
    'MINI_APP_GET_UNIONID_ERROR': {'code': 9007, 'msg': '小程序获取unionid错误'},

    # 10 配置
    'CFG_ADMIN_ID_NOT_EXIST': {'code': 10001, 'msg': '管理员id非空'},
    'CFG_ADMIN_QUERY_ERROR': {'code': 10002, 'msg': '查询管理员配置失败'},
    'CFG_CITY_PARAMS_NOT_EXIST': {'code': 10003, 'msg': '城市配置，关键参数不存在'},
    'CFG_PAY_NOT_FIND': {'code': 10005, 'msg': '支付配置未找到'},
    'CFG_THEME_NOT_FIND': {'code': 10006, 'msg': '模板未找到'},
    'CFG_CITY_NOT_FIND': {'code': 10007, 'msg': '城市未找到'},
    'CFG_ADDRESS_NOT_COMPLETE': {'code': 1008, 'msg': '地址信息不完整'},
    'CFG_ADDRESS_WRONG_DATA': {'code': 1009, 'msg': '数据错误,未指定分页属性'},
    'CFG_ADDRESS_NO_ID': {'code': 10010, 'msg': '未指定地址id'},
    'CFG_ADDRESS_EMPTY': {'code': 10011, 'msg': '未找到地址'},
    'CFG_ADDRESS_RIGHT_NOT_FOUND': {'code': 10012, 'msg': '未找到权限'},
    'CFG_ADDRESS_MODIFY_FAIL': {'code': 10013, 'msg': '数据修改失败'},
    'CFG_ADDRESS_DELETE_FAIL': {'code': 10014, 'msg': '数据删除失败'},
    'CFG_ADDRESS_SEARCH_CONTENT_NULL': {'code': 10015, 'msg': '搜索内容为空'},
    'CFG_LOGIS_DATA_EMPTY': {'code': 10016, 'msg': '未找到任何对应快递公司'},
    'CFG_SHOP_ORDER_VOERTIME_NONE': {'code': 10017, 'msg': '超时参数为空'},
    'CFG_SHOP_ORDER_CFG_FAIL': {'code': 10018, 'msg': '店铺订单超时配置失败'},
    'CFG_SHOP_ORDER_QUERY_FAIL': {'code': 10019, 'msg': '店铺订单查询失败'},
    'CFG_ADDRESS_CREATE_FAIL': {'code': 10020, 'msg': '地址创建失败'},
    'CFG_MESSAGE_OPENER_NOT_FOUND': {'code': 10021, 'msg': '消息开关记录查找失败'},
    'CFG_MESSAGE_OPENER_FAIL': {'code': 10022, 'msg': '消息开关设置失败'},
    'CFG_MESSAGE_MEDIA_ERROR': {'code': 10023, 'msg': '媒体类型错误'},
    'CFG_MESSAGE_SMS_ERROR': {'code': 10024, 'msg': '短信需要先充值'},
    'CFG_MESSAGE_WE_CHAT_TEMPLATE_ERROR': {'code': 10025, 'msg': '微信模板消息需要先公众号授权'},

    # 11 微信
    'WECHAT_AUTH_ERROR': {'code': 11001, 'msg': '微信授权失败'},
    'WECHAT_AUTH_PARAMS_NOT_EXIST': {'code': 11002, 'msg': '微信授权，参数为空'},
    'WECHAT_ACCESS_TOKEN_NOT_EXIST': {'code': 11003, 'msg': 'access_token不存在'},
    'WECHAT_JSAPI_TICKET_NOT_EXIST': {'code': 11004, 'msg': 'jsapi_ticket不存在'},
    'WECHAT_TOKEN_NOT_EXIST': {'code': 11005, 'msg': '公众号校检token缺失'},

    # 11.1 微信公众号相关
    'WECHAT_OPEN_TICKET_ERROR': {'code': 11101, 'msg': '平台ticket错误'},
    'WECHAT_OPEN_DATA_ERROR': {'code': 11102, 'msg': '平台授权数据错误'},
    'WECHAT_OPEN_GET_COMPONENT_ACCESS_TOKEN_FAILED': {'code': 11103, 'msg': '获取平台access_token失败'},
    'WECHAT_OPEN_GET_PRE_AUTH_CODE_FAILED': {'code': 11104, 'msg': '获取平台pre_auth_code失败'},
    'WECHAT_OPEN_GET_AUTH_URL_FAILED': {'code': 11105, 'msg': '获取公从号授权地址失败'},
    'WECHAT_OPEN_GET_AUTHORIZATION_INFO_FAILED': {'code': 11106, 'msg': '获取公众号授权信息失败'},
    'WECHAT_OPEN_GET_AUTHORIZER_INFO_FAILED': {'code': 11107, 'msg': '获取公众号信息失败'},
    'WECHAT_OPEN_GET_AUTHORIZER_INFO_EMPTY': {'code': 11108, 'msg': '未有公众号信息'},
    'WECHAT_OPEN_AUTH_REFRESH_FAILED': {'code': 11109, 'msg': '刷新公众号授权信息失败'},
    'WECHAT_OPEN_AUTHORIZER_TYPE_ERROR': {'code': 11110, 'msg': '公众号类型错误，必须是服务号'},
    'WECHAT_OPEN_CREATE_TEMPLATE_FAILED': {'code': 11111, 'msg': '创建公众号消息模板失败'},
    'WECHAT_TEMPLATE_NUM_EXCEED_LIMIT': {'code': 11112, 'msg': '公众号模板数量达到数量限制'},
    'WECHAT_OPEN_SEND_TEMPLATE_FAILED': {'code': 11113, 'msg': '发送公众号消息模板失败'},
    'QUERY_TEMPLATE_ID_ERROR': {'code': 11114, 'msg': '获取模板id失败'},
    #
    'WECHAT_CFG_DATA_ERROR': {'code': 11201, 'msg': '公众号配置信息有误'},

    # 12 统计
    'DATA_ORDER_PARAMS_NOT_EXIST': {'code': 12001, 'msg': '订单统计，参数非空'},
    # 12.1 页面事件
    'ST_CREATE_EVENT_FAILED': {'code': 12101, 'msg': '创建页面事件失败'},
    'ST_EVENT_NAME_NOT_MATCH': {'code': 12102, 'msg': '事件名称不匹配'},
    'ST_EVENT_DATA_FAILED': {'code': 12103, 'msg': '事件数据不正确'},

    # 13 店铺装修
    # 13.1 店铺模板初始化
    'DM_INIT_FAILED': {'code': 13101, 'msg': '初始化模板失败'},
    # 13.2
    'DM_CREATE_PAGE_PARAMS_NOT_EXIST': {'code': 13001, 'msg': '创建店铺page，参数非空'},
    'DM_JSON_ERROR': {'code': 13002, 'msg': '解析page json错误'},
    'DM_UPDATE_PAGE_PARAMS_NOT_EXIST': {'code': 13003, 'msg': '更新店铺page，参数非空'},
    'DM_SHOP_NOT_PERMISSION': {'code': 13004, 'msg': '你无权操作该page'},
    'DM_QUERY_PARAMS_NOT_EXIST': {'code': 13005, 'msg': '查询page,参数非空'},
    'DM_PAGE_NOT_FIND': {'code': 13006, 'msg': '页面未找到'},
    'DM_TEMP_PARAM_NOT_EXIST': {'code': 13007, 'msg': '临时页面参数非空'},
    'DM_PUBLISH_PARAM_NOT_EXIST': {'code': 13008, 'msg': '发布页面,参数非空'},
    'DM_TEMP_NOT_FIND': {'code': 13009, 'msg': '临时页面未找到'},
    'DM_UPDATE_HOMEPAGE_PARAMS_NOT_EXIST': {'code': 13010, 'msg': '设置主页，参数非空'},
    'DM_TEMP_NAV_CREATE_PARAMS_NOT_EXIST': {'code': 13011, 'msg': '创建临时页面，参数非空'},
    'DM_NAV_NOT_FIND': {'code': 13012, 'msg': '导航栏未找到'},
    'DM_NAV_UPDATE_FAIL': {'code': 13012, 'msg': '显示导航更新失败'},
    'DM_DELETE_TEMP_PAGE_PARAMS_NOT_EXIST': {'code': 13012, 'msg': '删除临时页面'},
    'DM_PUBLISH_PARAM_ERROR': {'code': 13013, 'msg': '参数错误'},
    'DM_PUBLISH_FAIL': {'code': 13014, 'msg': '发布失败'},
    'DM_PUBLISH_NOT_FOUND': {'code': 13015, 'msg': '发布页面未找到'},
    'DM_PUBLISH_DELETE_FAIL': {'code': 13016, 'msg': '删除失败'},
    'DM_PAGE_PARAM_ERROR': {'code': 13017, 'msg': '参数错误'},
    'DM_CHOOSE_SET_EXECUTE_FAIL': {'code': 13018, 'msg': '主题设置失败'},
    'DM_TEMP_PARAM_ERROR': {'code': 13019, 'msg': '页面参数有误'},
    'DM_CHOOSE_PAGE_EXECUTE_FAIL': {'code': 13020, 'msg': '模板默认页设置失败'},
    'DM_THEME_NOT_EXIST': {'code': 13021, 'msg': '查询的主题不存在'},
    'DM_PUBLISH_THEME_NOT_EXIST': {'code': 13022, 'msg': '该店铺尚未发布主题'},
    'DM_SHOP_THEME_NOT_EXIST': {'code': 13023, 'msg': '商店没有该副本'},
    'DM_COMPONENT_PARAMS_ERROR': {'code': 13024, 'msg': '组件列表格式错误'},
    'DM_UPDATE_COMP_FAIL': {'code': 13025, 'msg': '更新组件失败'},
    'DM_DELETE_PAGE_COMP_FAIL': {'code': 13026, 'msg': '删除主题页面和组件失败'},
    'DM_DELETE_COMP_LIST_FAIL': {'code': 13027, 'msg': '删除页面组件失败'},
    'DM_COPY_THEME_NOT_EXIST': {'code': 13028, 'msg': '复制的模板不存在'},
    'DM_HOMEPAGE_NOT_EXIST': {'code': 13029, 'msg': '已发布的店铺没有主页'},

    # 14 营销活动
    'PM_CREATE_PARAMS_NOT_EXIST': {'code': 14001, 'msg': '创建营销活动，参数不存在'},
    'PM_UPDATE_PARAMS_NOT_EXIST': {'code': 14002, 'msg': '更新营销活动，参数不存在'},
    'PM_ACTIVITY_NOT_FIND': {'code': 14003, 'msg': '营销活动未找到'},
    'PM_SHOP_NOT_PERMISSION': {'code': 14004, 'msg': '该店铺无权操作该营销活动'},
    'PM_GOODS_EXIST_ONLY_ONE': {'code': 14005, 'msg': '一个商品只能参加一个活动'},
    'PM_GOODS_GROUP_EXIST_ONLY_ONE': {'code': 14005, 'msg': '该分组已参与营销活动'},
    'PM_ONLY_ONE_ACTIVITY_ACTIVE': {'code': 14006, 'msg': '同一时间只允许一个活动生效'},
    'PM_QUERY_PARAMS_NOT_EXIST': {'code': 14007, 'msg': '查询营销活动，参数不存在'},
    'PM_ALL_GOODS_EXIST': {'code': 14008, 'msg': '存在营销活动，适用于所有商品'},
    'PM_GOODS_CATEGORY_EXIST_ONLY_ONE': {'code': 14009, 'msg': '该分类已参与营销活动'},
    'PM_DELETE_ACTIVITY_PARAMS_NOT_EXIST': {'code': 14010, 'msg': '删除营销活动，参数非空'},
    'PM_GOODS_NOT_PERMISSION': {'code': 14011, 'msg': '当前商品无法加入营销活动'},
    'PM_GOODS_GROUP_NOT_PERMISSION': {'code': 14012, 'msg': '当前商品分组无法加入营销活动'},
    'PM_CREATE_WALLET_PARAMS_NOT_EXIST': {'code': 14013, 'msg': '买家领取优惠券，关键参数不存在'},
    'PM_ACTIVITY_SHOP_NOT_MATCH': {'code': 14013, 'msg': '营销活动和店铺不匹配'},
    'PM_OUT_OF_BUY_VOL_LIMIT': {'code': 14014, 'msg': '优惠券超出限领数量'},
    'PM_STOCK_EMPTY': {'code': 14015, 'msg': '优惠券已被领光'},
    'PM_COUPON_USE_PARAMS_NOT_EXIST': {'code': 14016, 'msg': '使用优惠券失败，参数非空'},
    'PM_COUPON_CODE_NOT_FIND': {'code': 14017, 'msg': '优惠券未找到'},
    'PM_COUPON_CODE_NOT_VALID': {'code': 14018, 'msg': '优惠券已失效'},
    'PM_COUPON_QUERY_BUYER_PARAMS_NOT_EXIST': {'code': 14019, 'msg': '查询买家能够使用的优惠券，参数非空'},
    'PM_VALID_COUPON_NOT_FIND': {'code': 14020, 'msg': '无可用优惠券'},
    'PM_QUERY_PROMOTION_PARAMS_NOT_EXIST': {'code': 14021, 'msg': '营销插件--查询营销信息，参数非空'},
    'PM_QUERY_PROMOTION_ERROR': {'code': 14022, 'msg': '查询营销失败'},
    'PM_COUPON_GOODS_MONEY_NOT_ENOUGH': {'code': 14023, 'msg': '商品金额不满足优惠券使用条件'},
    'PM_LOCK_BUYER_COUPON_PARAMS_NOT_EXIST': {'code': 14024, 'msg': '锁定买家优惠券参数非空'},
    'PM_IS_DISABLED': {'code': 14025, 'msg': '活动不可用'},

    # 15 资金
    'FM_CREATE_REFUND_PARAMS_NOT_EXIST': {'code': 15001, 'msg': '创建退款请求，参数非空'},
    'FM_REFUND_NOTIFY_PARAMS_NOT_EXIST': {'code': 15002, 'msg': '退款回调，关键参数非空'},
    'FM_REFUND_EXPIRE': {'code': 15003, 'msg': '退款回调，过期'},
    'FM_REFUND_APPLY_NOT_PERMISSION': {'code': 15004, 'msg': '售后申请记录中，存在审核未通过或者未审核的情况'},
    'FM_REFUND_DOUBLE_APPLY': {'code': 15005, 'msg': '不允许重复申请退款记录'},
    'FM_QUERY_MONTH_DETAIL_ERROR': {'code': 15006, 'msg': '查询对账单报错'},
    'FM_SMS_BALANCE_ERROR': {'code': 15009, 'msg': '账户短信余额不足'},
    'FM_WITHDRAW_ERROR': {'code': 15010, 'msg': '提现金额大于账户余额或提现金额非正'},
    'FM_WITHDRAW_REVIEW_ERROR': {'code': 15011, 'msg': '该提现申请已审核'},
    'FM_ACCOUNT_ERROR': {'code': 15012, 'msg': '两次输入银行账户不一致'},
    'FM_WITHDRAW_REVIEW_STATUS_ERROR': {'code': 15013, 'msg': '审核状态错误'},
    'FM_WITHDRAW_ID_ERROR': {'code': 15014, 'msg': '未查询到此提现信息'},
    'FM_WITHDRAW_ACCOUNT_ERROR': {'code': 15015, 'msg': '未设置提现账户'},
    'FM_WITHDRAW_STATUS_PAY_ERROR': {'code': 15016, 'msg': '提现审核未通过或者未审核'},

    # 16 第三方
    # 16.1 物流
    'THIRD_PART_LOGISTICS_INCLUDE_FAIL': {'code': 16101, 'msg': '导入失败'},
    # 16.2 消息
    'THIRD_PART_MESSAGES_SEND_FAILED': {'code': 16201, 'msg': '消息发送失败'},
    # 16.3 验证码
    'THIRD_PART_VERIFY_CODE_FAILED': {'code': 16301, 'msg': '校验码不存在或已失效'},
    # 16.4 三方服务故障
    'THIRD_PART_SERVER_ERROR': {'code': 16401, 'msg': '第三方服务故障'},

    # 17 MQ消息
    'TASK_STOCK_MESSAGE_NONE': {'code': 17001, 'msg': '消息为空'},
    'TASK_STOCK_SENDMSG_FAIL': {'code': 17002, 'msg': '消息发送失败'},

    # 18 通知模块
    'NOTIFY_PARAMS_NOT_EXIST': {'code': 18003, 'msg': '通知参数为空'},
    'NOTIFY_SEND_FAIL': {'code': 18003, 'msg': '通知发送失败'},
    'NOTIFY_TEMPLATE_EX_FAIL': {'code': 18005, 'msg': '未找到消息模板'},
    'NOTIFY_OPENER_CLOSED': {'code': 18006, 'msg': '媒体消息开关关闭'},
    'NOTIFY_SEND_DATA_ERROR': {'code': 18007, 'msg': '消息参数错误'},
    'NOTIFY_SEND_MEDIA_ERROR': {'code': 18008, 'msg': '消息媒体错误'},
    'NOTIFY_WEIXIN_PARAMS_ERROR': {'code': 18009, 'msg': '消息媒体错误'},
    'NOTIFY_WEIXIN_TEMPLATE_ERROR': {'code': 18010, 'msg': '微信信息模板错误'},
    'NOTIFY_CREATE_PARAMS_NULL': {'code': 18011, 'msg': '通知记录操作参数非空'},
    'NOTIFY_EXECUTE_ERROR': {'code': 18012, 'msg': '通知记录数据库操作失败'},

    # 19 验证
    'IMAGE_VERIFY_ERROR': {'code': 19000, 'msg': '图形验证失败'},
    'MOBILE_FORMAT_ERROR': {'code': 19001, 'msg': '手机格式错误'},
    'VERIFY_CODE_ERROR': {'code': 19002, 'msg': '验证码错误'},

    # 20 rain card
    'RAINCARD_SKU_ID_NOT_PERMISSION': {'code': 20001, 'msg': '你无权操作该sku'},
    'RAINCARD_DELETE_PARAMS_NOT_EXIST': {'code': 20002, 'msg': 'raincard关键参数不存在'},

    # 21 资源库
    'CATEGORY_IN_CATEGORY_ERROR': {'code': 21001, 'msg': '该文件夹存在子文件夹，请先删除子文件夹'},
    'DATA_ONLY_FILE': {'code': 21002, 'msg': '只允许批量上传文件资源'},
    'DATA_ID_NOT_PARENT_ID': {'code': 21003, 'msg': '文件夹不能移动进它本身'},

    # 22 购物车
    'CART_PARAMS_DATA_ERROR': {'code': 22001, 'msg': '购物车参数数据错误'},
    'CART_DATA_ERROR': {'code': 22003, 'msg': '购物车数据错误'},

    # 23 客服配置
    'CODE_NOT_EXIST': {'code': 23001, 'msg': 'code不能为空'},

    # 24 消息推送
    'MESSAGE_SENDER_DATA_ERROR': {'code': 24001, 'msg': '发送者配置数据不正确'},
}
