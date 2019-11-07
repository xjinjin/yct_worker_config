#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import logging
# from logging.handlers import TimedRotatingFileHandler
from logging.handlers import RotatingFileHandler
import requests
import os

class get_log():
    def __init__(self):
        '''日志等级'''
        self.loglevel_1 = logging.NOTSET    # 0
        self.loglevel_2 = logging.DEBUG     # 10
        self.loglevel_3 = logging.INFO      # 20
        self.loglevel_4 = logging.WARNING   # 30
        self.loglevel_5 = logging.ERROR     # 40
        self.loglevel_6 = logging.CRITICAL  # 50
        '''日志格式'''
        self.formatter_1 = logging.Formatter('%(asctime)s %(message)s')
        self.formatter_2 = logging.Formatter('%(pathname)s--第%(lineno)d行--%(levelname)s--%(message)s')

    def config_log(self, filename=None):
        # 1.导入:__name__ == check_proxy  2.直接运行:__name__ == "__main__"
        logger = logging.getLogger('check_proxy')
        if not bool(filename):
            return self.config_stream_log(logger)
        else:
            return self.config_file_log(logger, filename)

    def config_file_log(self, logger, filename):
        logger.setLevel(self.loglevel_5)

        # '''屏幕输出'''
        # ch = logging.StreamHandler()
        # ch.setLevel(self.loglevel_5)
        # ch.setFormatter(self.formatter_1)
        # logger.addHandler(ch)

        '''定义文件流'''
        # fh = TimedRotatingFileHandler(filename=filename, when='s', interval=1)
        fh = RotatingFileHandler(filename=filename, maxBytes=512*1024*1024,backupCount=2)
        fh.setLevel(self.loglevel_5)
        fh.setFormatter(self.formatter_1)
        # fh.suffix = '.log'
        # fh.suffix = '%Y%m%d-%H%M.log'
        # fh.suffix = '%Y-%m-%d %H-%M-%S.log'
        logger.addHandler(fh)

        return logger

    def config_stream_log(self, logger):
        handler = logging.StreamHandler()
        handler.setFormatter(self.formatter_2)
        logger.addHandler(handler)
        logger.setLevel(self.loglevel_1)
        return logger

    def get_filesize(path: 'str'):
        '''获取文件的大小字节'''
        file_size = os.stat(path)
        return file_size.st_size

if __name__ == "__main__":  # 1.导入:__name__ == check_proxy  2.直接运行:__name__ == "__main__"

    current_dir = os.path.dirname(os.path.abspath(__file__))    # __file__表示显示文件当前的位置
    log_file = os.path.join(current_dir,'check_proxy.log')

    #自定义请求头信息
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
        }

    #指定url
    url = 'http://yct.sh.gov.cn/portal_yct/'

    #proxy
    # proxy =  {"http": "192.168.1.230:8888"}
    proxy =  {"http": "127.0.0.1:8888"}

    #发起请求
    try:
        response = requests.get(url=url, headers=headers, proxies=proxy, timeout=40)
    except Exception as e:
        # 1.记录错误日志
        # 2.docker restart yct_proxy_v1
        logger = get_log().config_log(log_file) # 自动创建check_proxy.log
        logger.error('%s' %e)
        os.system("docker restart yct_proxy_v1")
    # logger = get_log().config_log(log_file)
    # logger.error('test')
    # os.system("ls")

