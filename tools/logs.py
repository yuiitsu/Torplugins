# -*- coding:utf-8 -*-

"""
@author onlyfu
@time 2017/7/19
"""
import logging
import logging.config


class Logs(object):

    logger = None

    def __init__(self):
        self.logger = logging.getLogger()
        # handler = logging.StreamHandler()
        # formatter = logging.Formatter(
        #     '%(asctime)s %(levelname)-8s %(filename)s %(lineno)d : %(message)s')
        # handler.setFormatter(formatter)
        # self.logger.addHandler(handler)
        logging.basicConfig(format='%(asctime)s %(levelname)-8s %(filename)s %(lineno)d : %(message)s')
        self.logger.setLevel(logging.INFO)

    def get_logger(self):
        return self.logger


if __name__ == '__main__':
    logging.info('123')

