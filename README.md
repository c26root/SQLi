# SQLi



### 可部署多主机节点sqlmapapi来进行注入测试 (随机选择主机)
```
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
### 启动sqlmapapi
```
cd sqlmap
python sqlmapapi.py -s -H 0.0.0.0
```

### 测试
```
python main.py
```

```
[+] Host Number: 2
[+] Host List: [
  "localhost", 
  "127.0.0.1"
]
[GET] http://127.0.0.1:8775/admin/2872af061add7b2fea33e5b1f9434338/flush
[GET] http://127.0.0.1:8775/task/new
[POST] http://127.0.0.1:8775/scan/2f5d4e375952518c/start
{
  "url": "http://172.16.13.132/app.php?id=1*&user=a*", 
  "headers": [
    "X-Real-IP: 8.8.8.8*", 
    "Referer: http://172.16.13.132/app.php?id=1&user=a*", 
    "X-Forwarded-For: 8.8.8.8*", 
    "Client-IP: 8.8.8.8*", 
    "User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36*"
  ], 
  "flushSession": true, 
  "method": "GET"
}

```

```
curl http://127.0.0.1:8775/admin/2872af061add7b2fea33e5b1f9434338/list
```

```
{
    "tasks": {
        "2f5d4e375952518c": "terminated"
    },
    "tasks_num": 1,
    "success": true
}

```