# -*- coding:utf-8 -*-
# WEB 入口文件
# 通过web/conf/route.py文件来配置路由

import sys
# 设置环境，根据项目目录结构设置相对路径
sys.path.append("../")

# 配置文件
from conf.route import route, setting
# 父类
import source.controller as controller



if __name__ == '__main__':
    # 启动服务
    controller.server().start(route, setting)
