# sqli
## sqlmapapi
```
python main.py
{
  "url": "http://172.16.13.132/app.php?id=1*&user=a*", 
  "headers": "X-Real-IP: 8.8.8.8*\r\nReferer: http://172.16.13.132/app.php?id=1&user=a*\r\nX-Forwarded-For: 8.8.8.8*\r\nClient-IP: 8.8.8.8*\r\nUser-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36*", 
  "flushSession": true, 
  "method": "GET"
}
```