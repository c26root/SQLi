#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import sys
import json
from math import ceil
sys.path.append('../')
from config import DB_URL, DB_NAME, HOSTS

from flask import Flask, request, jsonify, abort, render_template, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)


# 连接MongoDB
client = MongoClient(DB_URL)
db = client[DB_NAME]

# 一页显示数量
show_size = 10


@app.route('/')
def main():
    return redirect(url_for('tasks'))


@app.route('/host')
def host():
    return json.dumps(HOSTS, indent=2)


@app.route('/host/stat')
def host_stat():
    ret = []
    for host in HOSTS:
        _host = host.split(':')[0]
        count = db.tasks.count({'host': _host})
        ret.append({
            'host': host,
            'task_number': count
        })
    return json.dumps(ret, indent=2)

@app.route('/tasks')
def tasks():
    page = request.args.get('page', 1, type=int)
    host = request.args.get('host')
    if host:
        total_size = db.tasks.count({'host': host})
    else:
        total_size = db.tasks.count()

    # 获取页数
    total_page = int(ceil(float(total_size) / show_size))
    # 初始化最少一页
    total_page = total_page if total_page else 1

    if page <= 0:
        return redirect((url_for('tasks')))
    elif page > total_page:
        page = total_page
        return redirect('{0}?page={1}'.format(url_for('tasks'), str(page)))
    if host:
        docs = db.tasks.find({'host': host}).skip(
            (page - 1) * show_size).limit(show_size)
    else:
        docs = db.tasks.find().skip((page - 1) * show_size).limit(show_size)

    result = []
    for doc in docs:
        doc['_id'] = str(doc['_id'])
        result.append(doc)
    return render_template('index.html', title='Tasks', result=result, show_size=show_size, total=total_size, current_page=page, total_page=total_page)
    return jsonify(result=result)


@app.route('/result')
def result():
    page = request.args.get('page', 1, type=int)
    host = request.args.get('host')
    if host:
        total_size = db.result.count({'host': host})
    else:
        total_size = db.result.count()
    # 获取页数
    total_page = int(ceil(float(total_size) / show_size))
    # 初始化最少一页
    total_page = total_page if total_page else 1

    if page <= 0:
        return redirect((url_for('result')))
    elif page > total_page:
        page = total_page
        return redirect('{0}?page={1}'.format(url_for('result'), str(page)))
    if host:
        docs = db.result.find({'host': host}).skip(
            (page - 1) * show_size).limit(show_size)
    else:
        docs = db.result.find().skip((page - 1) * show_size).limit(show_size)

    result = []
    for doc in docs:
        doc['_id'] = str(doc['_id'])
        data = doc['data']
        payload = []
        if len(data) == 1:
            doc['parameter'] = data[0]['value'][0]['parameter']
            for k, v in data[0]['value'][0]['data'].iteritems():
                payload.append(v.get('payload'))
        else:
            doc['parameter'] = data[1]['value'][0]['parameter']
            for k, v in data[1]['value'][0]['data'].iteritems():
                doc['payload'] = v
                payload.append(v.get('payload'))

        doc['payload'] = json.dumps(payload)
        doc['payload'] = payload[0]

        result.append(doc)
    return render_template('result.html', title='Result', result=result, show_size=show_size, total=total_size, current_page=page, total_page=total_page, host=host)


@app.route('/result/<taskid>')
def view(taskid):

    docs = db.result.find_one({'taskid': taskid})
    if not docs:
        abort(404)
    docs['_id'] = str(docs['_id'])
    del docs['options']
    # return render_template('item.html', result=json.dumps(docs, indent=2))
    return jsonify(docs)


@app.route('/result/del')
def result_del():
    taskid = request.args.get('taskid', '')
    referer = request.headers.get('Referer')
    if not taskid:
        return abort(403)
    db.result.remove({'taskid': taskid})
    return redirect(referer) if referer else redirect(url_for('result'))
    # return jsonify(code=200, msg='del success')


@app.errorhandler(404)
def page_not_found(error):
    return jsonify({
        'code': 404,
        'msg': 'Not Found'
    }), 404


@app.errorhandler(403)
def Forbidden(error):
    return jsonify({
        'code': 403,
        'msg': 'Forbidden'
    }), 403


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        'code': 500,
        'msg': 'Internal Server Error'
    }), 500


# 检查是否合法ObjectId
def is_valid_id(_id):
    if len(_id) != 24:
        return False
    try:
        _id.decode('hex')
        return True
    except Exception as e:
        return False

if __name__ == '__main__':
    app.debug = True
    app.run(
        host='0.0.0.0',
        port=8000,
        threaded=True)
