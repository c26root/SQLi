#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import random
from config import hosts, timeout, headers, default_admin_id
from sqlmapapi import SQLMapApi
from utils import Url

try:
    basestring
except NameError:
    basestring = string

# 获取节点列表


def get_host_list():
    return hosts

# 随机选择一个节点


def get_host():
    # 初始化
    host, port, admin_id = '127.0.0.1', 8775, default_admin_id
    host = random.choice(hosts)
    pairs = host.split(':')

    if len(pairs) == 2:
        host = pairs[0]
        port = int(pairs[1])
        admin_i = admin_id
    elif len(pairs) == 3:
        host = pairs[0]
        port = int(pairs[1])
        admin_id = pairs[2]
    else:
        print '主机端口格式错误'
        return False

    return host, port, admin_id

# 生成选项


def get_options(url, data='', cookie='', referer=''):

    method = 'GET'
    if data:
        method = 'POST'

    headers['Referer'] = referer or url

    if cookie:
        headers['Cookie'] = cookie

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
    if data and isinstance(data, basestring):
        data = dict(Url.qs_parse(data))
        data = Url.build_qs(data)
        data = data.replace('&', '*&') + '*'

    # 污染头部
    for k, v in headers.iteritems():
        if k == 'Cookie':
            headers[k] = v.replace(';', '*;') + '*'
        else:
            headers[k] = v + '*'

    # 转成HTTP头
    headers_str = '\r\n'.join(['{}: {}'.format(k, v)
                               for k, v in headers.iteritems()])

    options = {}
    options['url'] = url
    # 使用自定义头部
    options['headers'] = headers_str

    # 不使用缓存记录
    options['flushSession'] = True
    if data:
        options['method'] = 'POST'
        options['data'] = data
    else:
        options['method'] = 'GET'

    return options


def start_task(options):

    # 创建任务
    taskid = api.task_new()
    if not taskid:
        print u'创建任务失败'
        exit()
    # 配置参数 开始任务
    api.scan_start(taskid, options=options)


if __name__ == '__main__':

    host, port, admin_id = get_host()

    api = SQLMapApi(host, port, admin_id=admin_id, timeout=5)

    print '[HOST LIST]'
    for host in hosts:
        print '[HOST]', host
    print

    url = 'http://172.16.13.132/app.php?id=1&user=a'
    data = ''
    cookie = ''

    # 清除所有任务
    api.admin_flush()
    options = get_options(url, data, cookie)
    print json.dumps(options, indent=2)
    for i in options['headers'].split('\r\n'):
        print i
    start_task(options)
