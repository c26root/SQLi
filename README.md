# SQLi



### 可部署多主机节点sqlmapapi来进行SQL注入测试(随机选择主机)

```
pip install requests
pip install eventlet

vim config.py
```
```
# API主机列表 格式 host:port:admin_id 如果不填写
hosts = [
    'localhost:8080',
    '127.0.0.1:8775:2872af061add7b2fea33e5b1f9434338',
]

# 默认管理id 建议修改sqlmap/lib/utils/api.py中admin_id为固定hash
default_admin_id = '182e2aab18e1e96a5e4d8be2411d56d3'

...
```
### 在主机节点上启动sqlmapapi(使用Eventlet/Gevent/Tornaod作为WSGI Server)
```
cd sqlmap
python sqlmapapi.py -s -H 0.0.0.0 --adapter eventlet
```

### 测试
```
python run.py
```

```
#######################################################################################################################
2017-02-12 12:49:24,504 INFO Starting new HTTP connection (1): test.com
2017-02-12 12:49:24,728 DEBUG "GET /admin/182e2aab18e1e96a5e4d8be2411d56d3/list HTTP/1.1" 200 105
2017-02-12 12:49:24,730 INFO [test.com] Task Total Number: 1
2017-02-12 12:49:24,730 INFO [test.com] Tasks: {
  "4c1a3623fe710ba2": "running"
}
2017-02-12 12:49:24,731 INFO Starting new HTTP connection (1): hk.test.com
2017-02-12 12:49:24,836 DEBUG "GET /admin/182e2aab18e1e96a5e4d8be2411d56d3/list HTTP/1.1" 200 105
2017-02-12 12:49:24,837 INFO [hk.test.com] Task Total Number: 1
2017-02-12 12:49:24,837 INFO [hk.test.com] Tasks: {
  "00651838ed775d27": "running"
}
2017-02-12 12:49:24,838 INFO Starting new HTTP connection (1): tokyo.test.com
2017-02-12 12:49:24,974 DEBUG "GET /admin/182e2aab18e1e96a5e4d8be2411d56d3/list HTTP/1.1" 200 105
2017-02-12 12:49:24,975 INFO [tokyo.test.com] Task Total Number: 1
2017-02-12 12:49:24,975 INFO [tokyo.test.com] Tasks: {
  "170898dd56a79c14": "running"
}
2017-02-12 12:49:24,977 INFO Starting new HTTP connection (1): tokyo2.test.com
2017-02-12 12:49:25,100 DEBUG "GET /admin/182e2aab18e1e96a5e4d8be2411d56d3/list HTTP/1.1" 200 185
2017-02-12 12:49:25,101 INFO [tokyo2.test.com] Task Total Number: 3
2017-02-12 12:49:25,101 INFO [tokyo2.test.com] Tasks: {
  "17d7397f3616b27c": "running",
  "4fa844fd53921cf7": "running",
  "a4c982fc6cad102f": "running"
}
#######################################################################################################################
2017-02-12 12:49:25,103 INFO Starting new HTTP connection (1): tokyo2.test.com
2017-02-12 12:49:25,218 DEBUG "GET /admin/182e2aab18e1e96a5e4d8be2411d56d3/list HTTP/1.1" 200 185
2017-02-12 12:49:25,222 INFO Starting new HTTP connection (1): tokyo2.test.com
2017-02-12 12:49:25,338 DEBUG "GET /task/new HTTP/1.1" 200 58
2017-02-12 12:49:25,340 INFO Starting new HTTP connection (1): tokyo2.test.com
2017-02-12 12:49:25,466 DEBUG "POST /scan/08755b3b11f9c04c/start HTTP/1.1" 200 47
2017-02-12 12:49:25,468 INFO Create Task Success, Task Id: [08755b3b11f9c04c]
2017-02-12 12:49:25,468 INFO [08755b3b11f9c04c] Task Options: {
  "url": "http://test.com:82/api.php?username=a1*",
  "headers": [
    "Client-IP: 8.8.8.8*",
    "Accept-Encoding: gzip, deflate, sdch",
    "X-Forwarded-For: 1.1.1.1*",
    "User-Agent: 132*",
    "Cookie: a=1*",
    "X-Real-IP: 8.8.8.8*"
  ],
  "flushSession": true,
  "method": "GET"
}
2017-02-12 12:49:25,468 INFO Sleep 5s

```