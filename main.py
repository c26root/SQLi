#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import random
from config import hosts, timeout, headers
from sqlmapapi import SQLMapApi
from utils import Url

# 获取节点列表
def get_host_list():
    return hosts

# 随机选择一个节点
def get_host():
    host, port = 'localhost', 8775
    host = random.choice(hosts)
    s = host.split(':')
    if len(s) != 2:
        print '主机端口格式错误'
        return False
    host = s[0]
    port = int(s[1])
    return host, port


def start_task(url, data=''):
    method = 'GET'
    if data:
        method = 'POST'

    headers['Referer'] = url
    headers[
        'User-Agent'] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
    headers['X-Forwarded-For'] = '8.8.8.8'
    headers['Client-IP'] = '8.8.8.8'
    headers['X-Real-IP'] = '8.8.8.8'
    headers['Cookie'] = 'userid=1; user=2; password=123'

    # 污染URL
    parse = Url.url_parse(url)
    query = parse.query
    if not query:
        query = url
    qs = Url.qs_parse(query)
    for i in qs:
        qs[i] += '*'
    qs = Url.urldecode(Url.build_qs(qs))
    url = Url.url_unparse(
        (parse.scheme,
         parse.netloc,
         parse.path,
         parse.params,
         qs,
         parse.fragment)
    )

    # 污染POST数据
    if data:
        data = dict(Url.qs_parse(data))
        # for k in data.keys():
        #   data[k] += '*'
        # data = Url.build_qs(data).replace('%2A', '*')
        data = Url.build_qs(data)
        data = data.replace('&', '*&') + '*'

    # 污染头部
    for k, v in headers.iteritems():
        if k == 'Cookie':
            headers[k] = v.replace(';', '*;') + '*'
        else:
            headers[k] = v + '*'

    # 相关污染数据
    print
    print '[URL] {}'.format(url)
    if data:
        print '[POST_DATA] {}'.format(data)
    print '[HEADER]'
    print json.dumps(headers, indent=2)
    print

    headers_str = '\r\n'.join(['{}: {}'.format(k, v)
                               for k, v in headers.iteritems()])

    options = {}
    options['url'] = url
    # Custom Headers
    options['headers'] = headers_str
    # Flush Session Log
    options['flushSession'] = True
    if data:
        options['method'] = 'POST'
        options['data'] = data
    else:
        options['method'] = 'GET'

    # 创建新任务
    taskid = api.task_new()
    if not taskid:
        print u'创建任务失败'

    # 配置参数 开始任务
    # api.option_set(taskid, options=options)
    api.scan_start(taskid, options=options)


if __name__ == '__main__':


    admin_id = '18317be61d15cbb1c37e5ae14301a63c'
    host, port = get_host()
    api = SQLMapApi(host, port, admin_id=admin_id, timeout=5)

    print '[HOST LIST]'
    for host in hosts:
        print '[HOST]', host
    print
    
    print api.get_info()
    print


    url = 'http://172.16.13.132/app.php?id=1&user=a'

    data=''

    api.admin_flush()

    start_task(url, data=data)