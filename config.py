#!/usr/bin/env python
# -*- coding: utf-8 -*-

hosts = [
	'localhost:8775',
	'127.0.0.1:8775'
]
timeout = 5
user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"

headers = {
    'Referer': 'https://www.baidu.com/',
    'User-Agent': user_agent,
    'X-Forwarded-For': '8.8.8.8',
    'Client-IP': '8.8.8.8',
    'X-Real-IP': '8.8.8.8'
}

pollution_headers = ('Referer', 'User-Agent', 'X-Forwarded-For', 'Client-IP', 'X-Real-IP', )