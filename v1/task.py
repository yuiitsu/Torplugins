# -*- coding: utf-8 -*-

"""
@author: Yuiitsu
@file: task.py
@time: 2018/2/8 0:46
"""
from celery import Celery

celery = Celery('tasks', broker='redis://121.40.116.65:6379/0')

if __name__ == '__main__':
    celery.start()
