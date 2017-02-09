#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import time
import random
import logging

from config import HOSTS, TIMEOUT, DEFAULT_ADMIN_ID
from config import HEADERS

from sqlmapapi import SQLMapApi
from utils import Url


try:
    basestring
except NameError:
    basestring = string


# 随机选择一个节点


def get_host():
    # 初始化
    host, port, admin_id = '127.0.0.1', 8775, DEFAULT_ADMIN_ID
    host = random.choice(HOSTS)
    pairs = host.split(':')

    if len(pairs) == 2:
        host = pairs[0]
        port = int(pairs[1])
        admin_i = admin_id
    elif len(pairs) == 3:
        host = pairs[0]
        port = int(pairs[1])
        admin_id = pairs[2] or admin_id
    else:
        print '主机端口格式错误'
        return False

    return host, port, admin_id

def get_all_host():
    ret = []
    for i in HOSTS:
        host, port, admin_id = '127.0.0.1', 8775, DEFAULT_ADMIN_ID
        pairs = i.split(':')

        if len(pairs) == 2:
            host = pairs[0]
            port = int(pairs[1])
            admin_i = admin_id
        elif len(pairs) == 3:
            host = pairs[0]
            port = int(pairs[1])
            admin_id = pairs[2] or admin_id
        else:
            print '主机端口格式错误'
            return False
        ret.append((host, port, admin_id))
    return ret

# 生成选项
def get_options(url, data='', cookie='', referer=''):

    method = 'GET'
    if data:
        method = 'POST'
    headers = HEADERS.copy()
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
        logging.info(u'创建任务失败')
        # print u'创建任务失败'
        return 
    # 配置参数 开始任务
    api.scan_start(taskid, options=options)

if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')

    print '[+] Host Number:', len(HOSTS)
    print '[+] Host List:',
    print json.dumps([host.split(':')[0] for host in HOSTS], indent=2)


    http = {
        # 'url': 'http://172.16.13.132/app.php?id=1&user=a',
        'url': 'http://daza.im:82/api.php?username=a1',
        'data': '',
        'cookie': '',
    }


    # 清除所有任务
    # if api.admin_flush():
    #     logging.info('flush tasks success')



    while 1:

        for host in get_all_host():
            host, port, admin_id = host
            api = SQLMapApi(host, port, admin_id=admin_id, timeout=TIMEOUT)
            admin_list = api.admin_list()
            if admin_list:
                tasks = admin_list.get('tasks')
                logging.info('[{0}] tasks total number: {1}'.format(host, len(tasks)))
                for taskid in tasks:
                    status = tasks.get(taskid)

                    # 处理跑完的和没有跑起来的
                    if status in ('terminated', 'not running'):
                        # 跑完的获取结果查看是否有结果
                        if status == 'terminated':
                            task_data = api.scan_data(taskid)
                            if task_data.get('data'):
                                logging.info('inject task id: {}'.format(taskid))
                                # print task_data
                        result = api.task_delete(taskid)
                        if result.get('success'):
                            logging.info('delete task id: {}'.format(taskid))

            
            # 获取主机
            host, port, admin_id = get_host()
            
            api = SQLMapApi(host, port, admin_id=admin_id, timeout=TIMEOUT)
            
            admin_list = api.admin_list()
            if admin_list:
                tasks = admin_list.get('tasks')
                if len(tasks) >= 5:
                    logging.info('Queue Full')
                    time.sleep(2)
                    continue
            # 获取发送选项
            url, data, cookie = http.get('url'), http.get('data'), http.get('cookie')
            options = get_options(url, data, cookie)        
            # 开始任务
            start_task(options)
            options['headers'] = options['headers'].split('\r\n')
            print json.dumps(options, indent=2)
            
            logging.info('sleep 5s')
            time.sleep(5)
