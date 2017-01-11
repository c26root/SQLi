# sqli



### 可部署多节点sqlmapapi来进行注入测试

### 启动sqlmapapi [修改api.py]
```
cd sqlmap
python sqlmapapi.py -s -H 0.0.0.0
```
### 测试
```
python main.py

[options]
{
  "url": "http://172.16.13.132/app.php?id=1*&user=a*", 
  "headers": "X-Real-IP: 8.8.8.8*\r\nReferer: http://172.16.13.132/app.php?id=1&user=a*\r\nX-Forwarded-For: 8.8.8.8*\r\nClient-IP: 8.8.8.8*\r\nUser-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36*", 
  "flushSession": true, 
  "method": "GET"
}

X-Real-IP: 8.8.8.8*
Referer: http://172.16.13.132/app.php?id=1&user=a*
X-Forwarded-For: 8.8.8.8*
Client-IP: 8.8.8.8*
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36*

curl http://127.0.0.1:8775/admin/182e2aab18e1e96a5e4d8be2411d56d3/list


{
    "tasks": {
        "a69da2949e1d7148": "not running"
    }, 
    "tasks_num": 1, 
    "success": true
}

```