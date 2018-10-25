#!/usr/bin/env python
# encoding: utf-8

"""
@version: python37
@author: Geoffrey
@file: settings.py
@time: 18-10-25 下午3:20
"""

# Mysql数据库配置
MYSQL_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': '0',
    'db': '今日头条',
    'charset': 'utf8'
}

# mongodb 数据库配置
MONGO_CONFIG = ['192.168.62.35:1806, '
              '192.168.62.240:1806, '
              '192.168.62.23:1806, '
              '192.168.62.32:1806, '
              '192.168.62.25:1806, '
              '192.168.62.28:1806, '
              '192.168.62.241:1806']

KEY_WORD = '三里屯'

GROUP_START = 0,
GROPE_END = 10,