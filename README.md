# sqli


```
可部署多节点sqlmapapi来进行注入测试
```
```
cd sqlmap
python sqlmapapi.py -s -H 0.0.0.0
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

```