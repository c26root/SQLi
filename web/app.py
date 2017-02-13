#!/usr/bin/env python
# -*- encoding: utf-8 -*-


from flask import Flask, jsonify, abort
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)


# 数据库配置
DB_HOST = '172.16.13.135'
DB_PORT = 27017
DB_NAME = 'sqli'
DB_URL = 'mongodb://{}:{}'.format(DB_HOST, DB_PORT)

# 连接MongoDB
client = MongoClient(DB_URL)
db = client[DB_NAME]


@app.route('/tasks')
def main():
    docs = db.tasks.find()
    result = []
    for doc in docs:
        doc['_id'] = str(doc['_id'])
        result.append(doc)
    return jsonify(result=result)


@app.route('/<taskid>')
def view(taskid):

    if not is_valid_id(taskid):
       abort(403)

    docs = db.result.find_one({'_id': ObjectId(taskid)})
    if not docs:
        abort(404)

    docs['_id'] = str(docs['_id'])
    return jsonify(docs)


@app.errorhandler(404)
def page_not_found(error):
    return jsonify({
        'code': 404,
        'msg': 'Not Found'
    }), 404


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        'code': 500,
        'msg': 'Internal Server Error'
    }), 500


@app.errorhandler(403)
def unauthorized(error):
    return jsonify({
        'code': 403,
        'msg': 'Forbidden'
    }), 403


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
