#!/usr/bin/env python
# -*- coding: utf-8 -*-


# API主机列表
HOSTS = [
    # 'localhost:8775',
    'daza.im:8775',
    'hk.daza.im:8775',
    'tokyo.daza.im:8775',
]

# 默认管理id 建议修改sqlmap/lib/utils/api.py中admin_id为固定hash
DEFAULT_ADMIN_ID = '182e2aab18e1e96a5e4d8be2411d56d3'

# 超时时间
TIMEOUT = 5

USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"

# 需要污染的头部
HEADERS = {
    'User-Agent': USER_AGENT,
    'X-Forwarded-For': '8.8.8.8',
    'Client-IP': '8.8.8.8',
    'X-Real-IP': '8.8.8.8'
}

# 定期轮询时间
SLEEP_TIME = 5

# 单个节点最大任务数
MAX_TASK_NUMBER = 5


# 数据库连接配置
DB_HOST = '172.16.13.135'
DB_PORT = 27017
DB_NAME = 'passive'
DB_URL = 'mongodb://{0}:{1}'.format(DB_HOST, DB_PORT)


# 需要污染的头部
POLLUTION_HEADERS = (
    'Referer', 'User-Agent', 'X-Forwarded-For', 'Client-IP', 'X-Real-IP', )
