#!/usr/bin/env python
# -*- coding: utf-8 -*-

# API主机列表
hosts = [
    'localhost:8775',
    '127.0.0.1:8775'
]

# 管理id 建议修改sqlmapapi中admin_id为固定hash
admin_id = '182e2aab18e1e96a5e4d8be2411d56d3'

# 超时时间
timeout = 5

user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"

headers = {
    'User-Agent': user_agent,
    'X-Forwarded-For': '8.8.8.8',
    'Client-IP': '8.8.8.8',
    'X-Real-IP': '8.8.8.8'
}

# 需要污染的头部
pollution_headers = (
    'Referer', 'User-Agent', 'X-Forwarded-For', 'Client-IP', 'X-Real-IP', )
