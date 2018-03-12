# -*- coding:utf-8 -*-

"""
@author: delu
@file: cachekey_predix.py
@time: 17/4/13 下午3:01
"""


class CacheKeyPredix(object):

    # 用户管理

    # 管理员分组id
    GROUP_ID = 'group_id'
    # 管理员账户id
    ACCOUNT_ID = 'account_id'
    # 管理员id
    ADMIN_ID = 'admin_id'
    # 管理员id
    UID = 'uid'
    # 店铺id
    SHOP_ID = 'shop_id'
    # 店铺ID和二级域名映射
    DOAMIN_SHOP_ID = 'shop:domain:'
    # 平台管理员token前缀
    SUPERADMIN_TOKEN = 'superadmin_token_'
    # 管理员token前缀
    ADMIN_TOKEN = 'admin_token_'
    # 买家token前缀
    BUYER_TOKEN = 'buyer_token_'
    # 买家地址编号
    BUYER_ADDR_NO = 'buyer_addr_no'
    # 买家id
    BUYER_ID = 'buyer_id'
    # 微信小程序 - code
    MINI_APP_CODE = 'mini_app_code_'
    # 商品SKU库存
    GOODS_SKU_STOCK = 'sku:stock:'
    # 订单基础id，用于生成订单号
    ORDER_BASE_ID = 'order_base_id'
    # 退款批次号基础no,用于生成退款批次号
    BATCH_BASE_NO = 'batch_base_no'
    # 微信小程序，模板消息发送队列
    MINI_APP_MODEL_MESSAGE_USER = 'mini_app_model_message_user_'
    # 微信小程序access_token
    MINI_APP_ACCESS_TOKEN = 'mini_app_access_token'
    # 梅西闪闪购的Access token
    MACYS_FLASH_SALE_ACCESS_TOKEN = 'macys_flash_sale_access_token'
    # 物流模板编号
    GOODS_FARETMPLT_NO = 'goods_faretmplt_no'
    # 微信token
    WECHAT_ACCESS_TOKEN = 'wechat_access_token'
    # 微信jsapi信息
    WECHAT_JSAPI = 'wechat_jsapi'
    # 微信jsapi_ticket
    WECHAT_JSAPI_TICKET = 'wechat_jsapi_ticket'
    # 修改库存销量
    UPDATE_STOCK_SALE = 'update_stock_sale'
    # 临时page_id
    TEMP_PAGE_ID = 'temp_page_id'
    # 任务
    TASK_DATA_LIST = 'task_data_list'
    # 失败任务队列
    ERROR_TASK_DATA_LIST = 'error_task_data_list'
    # 营销活动前缀
    PM = 'pm_'
    # 优惠券库存
    PM_COUPON_STOCK = 'coupon:stock:'
    # 全部商品
    PM_ALL_GOODS = 'pm_all_goods'
    # 买家已领取的优惠券数量
    BUYERWALLET = 'buyerwallet_'
    # 买家参与的优惠券活动
    ALL_BUYERWALLET = 'all_buyerwallet_'
    # 订单支付缓存
    ORDER_PAY = 'order_pay_'
    # 充值订单支付缓存
    PAY_RECORD = 'pay_record_'
    # 订单支付回调缓存
    ORDER_NOTIFY = 'order_notify_'
    # 定时任务订单过期
    SCHEDULE_ORDER_EXPIRE = 'schedule_order_expire_'
    # 短信定时任务订单过期
    ORDER_SMS_NOTIFY_EXPIRE = 'order_sms_notify_expire_'
    # 微信定时任务订单过期
    ORDER_WECHAT_NOTIFY_EXPIRE = 'order_wechat_notify_expire_'
    # 验证码
    VERIFY_CODE = 'verify:code:'
    # 充值短信条数
    SMS_BALANCE = 'sms:balance:'
    # 商品基本信息
    GOODS_INFO = 'goods:info:'
    # 商品所有SKU
    GOODS_SKU_ALL = 'goods:sku:all:'
    # 商品所属分组
    GOODS_GROUP = 'goods:group:'
    # SKU信息，包含GOODS信息
    SKU_INFO = 'sku:info:'
    # 店铺支付参数
    SHOP_PAYMENT = 'shop_payment_'
    # 店铺管理员配置
    ADMIN_CONFIG = 'admin_config_'
    # 税率缓存
    HSCODE = 'hscode_'

    # 商品信息md5,更新商品时先去缓存比对
    GOODS_MD5 = 'goods_md5_'
    # 发送给osm的订单队列
    OMS_SALES_ORDER = 'oms_sales_order'
    # 发送给osm的用户队列
    OMS_BUYER_INFO = 'oms_buyer_info'
    # 发送给crm的用户队列
    CRM_BUYER_INFO = 'crm_buyer_info'
    # 仓库对应的物流模板
    WAREHOUSE_FARE_TEMPLATE = 'fare_template_'
    # 店铺的物流模板
    SHOP_FARE_TEMPLATE = 'fare_template_'
    # 梅西商品信息
    MACYS_GOODS = 'macys_goods_'
    # 梅西商品详情
    MACYS_GOODS_DETAIL = 'macys_goods_detail_'
    # 梅西商品对应的sku信息
    MACYS_GOODS_SKUS = 'macys_goods_skus_'
    # 梅西闪闪购活动信息
    MACYS_FLASH_ACTIVITY = 'macys_flash_activity_'
    MACYS_FLASH_SALE_STOCK = 'macys_flash_sale_stock_'
    MACYS_FLASH_SALE_START = 'macys_flash_sale_start_'
    MACYS_FLASH_SALE_END = 'macys_flash_sale_end_'
    MACYS_FLASH_SALE_NOTIFY = 'macys_flash_sale_notify_'
    MACYS_FLASH_SALE_ACTIVITY_PURCHASE_LIMITATION = 'macys_flash_sale_activity_purchase_limitation_'
    # 某闪购活动的订单
    MACYS_FLASH_SALE_PARENT_ORDER = 'macys_flash_sale_parent_order_'
    # 物流模板对应的物流信息
    FARE = 'fare_'
    # 梅西订单基础id，用于生成订单号
    MACYS_ORDER_BASE_ID = 'macys_order_base_id'
    # 梅西订单基础id，用于生成订单号
    MACYS_FLASH_ORDER_BASE_ID = 'macys_flash_order_base_id'
    # 梅西实时检测库存的授权token
    MACYS_STOCK_OAUTH_TOKEN = 'macys_stock_oauth_token'



