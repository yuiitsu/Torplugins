# -*- coding:utf-8 -*-

"""
@author: delu
@file: constants.py
@time: 17/4/12 下午2:22
"""


class Constants(object):
    SELLER_TYPE = 'seller'
    BUYER_TYPE = 'buyer'
    SUPER_ADMIN_TYPE = 'super_admin'
    ADMIN_TYPE = 'admin'

    SCEN_TYPE_WECHAT = 2
    SCEN_TYPE_FLASH_SALE = 10
    SCEN_TYPE_RAIN_CARD = 11

    # 支付
    PAY_TYPE_WECHAT = 3
    PAY_TYPE_ALIPAY = 1
    PAY_SUB_TYPE_WECHAT = 1
    PAY_SUB_TYPE_ALIPAY = 3

    # 订单状态
    # 未支付
    ORDER_WAIT_PAY = 1
    # 未发货
    ORDER_PAY_SUCCESS = 2
    # 已发货
    ORDER_SEND = 3
    # 已收货
    ORDER_RECEIVED = 4
    # 申请售后中
    ORDER_APPLY = 5
    # 已完成
    ORDER_SETTLED = 10
    # 已结束
    ORDER_FINISH = 7
    # 超卖
    ORDER_OVERBUY = 8
    # 已过期
    ORDER_EXPIRE = -1
    # 已关闭
    ORDER_CLOSE = -2

    # 母单状态
    # 未支付
    PARENT_ORDER_WAIT_PAY = 1
    # 正在处理中
    PARENT_ORDER_PROCESSING = 2
    # 已完成
    PARENT_ORDER_FINISH = 3

    # 售后审核状态
    ORDER_APPROVE_NOT_AUTH = 1
    ORDER_APPROVE_SUCCESS = 2
    ORDER_APPROVE_FAIL = -1

    # 售卖渠道
    SALE_CHANNEL = {
        1: '在线商城',
        2: 'raincard'
    }

    # 营销活动适用范围
    PM_ALL_GOODS = -1
    PM_GOODS = 1
    PM_GOODS_GROUP = 2
    PM_GOODS_CLASS = 3
    PM_BRAND = 4

    PM_COUPON = 'coupon'
    PM_PROMO_CODE = 'promo_code'
    PM_FULL_CUT = 'full_cut'

    # 购物车选中状态
    # 全部选中
    SHOPPING_CART_SELECT_ALL = -1
    # 全部取消
    SHOPPING_CART_UNSELECT_ALL = -2
    # 收款方式
    # 代收
    DIRECTION_OTHER = 1
    # 自收
    DIRECTION_SELF = 2

    # 发货通知
    SEND_NOTIFY = '1'
    # 订单催付
    NO_PAY_NOTIFY = '2'
    # 付款成功
    PAY_SUCCESS_NOTIFY = '3'
    # 退款成功
    REFUND_SUCCESS_NOTIFY = '4'
    # 退款失败
    REFUND_FAIL_NOTIFY = '5'
    # 售后未通过
    AFTER_SALE_APPLY_FAILED = '6'

    # 微信
    MEDIA_TYPE_WEIXIN = '2'
    # 短信
    MEDIA_TYPE_SMS = '1'
    # 邮件
    MEDIA_TYPE_EMAIL = '3'

    # 资金，收支类型
    # 订单收入
    FM_ORDER_INCOME = 1
    # 订单退款
    FM_ORDER_REFUND = 2

    # 境内仓库id列表
    DOMESTIC_WAREHOUSE_ID_LIST = [0, 1, 2]
    # 境外仓库id列表
    ABROAD_WAREHOUSE_ID_LIST = [3]

    # 订单取消
    # 默认取消原因
    DEFAULT_CANCEL_CODE = 4
    # 平台管理员取消
    PLATFORM_CANCEL = 5

    # 订单退款
    # 未退款
    NOT_REFUND = 0
    # 退款成功
    REFUND_SUCCESS = 1
    # 退款失败
    REFUND_FAIL = 2

    # 商户提现
    # 未审核
    NOT_REVIEW = '0'
    # 审核通过
    REVIEW_SUCCESS = '1'
    # 审核未通过
    REVIEW_FAIL = '2'
    # 转账处理中
    GIRO_PROCESSING = '3'
    # 已转账
    GIRO_SUCCESS = '4'
    # 转账失败
    GIRO_FAIL = '5'
