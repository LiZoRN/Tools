# Server Monitor

## 1. 环境安装：
### 1.1 安装Python

下载[python](https://www.python.org/downloads/)

注意：支持python 3.5+ 或者 python 2.7+，一般老点的服务器只支持安装python2.7.

### 1.2 安装库
进入工程根目录，执行:
```pip install -r requirements.txt```

        
## 2. 运行monitor api服务

```python monitorRestApi.py -h```

    Usage: monitorRestApi [-d "logpath."]  [-t "interval."] [-i "ip."] [-u "user."] [-p "password."] [-m "mode."]

    Copyright 2016 Ningbo Saturn

    Options:
      --version             show program's version number and exit
      -h, --help            show this help message and exit
      -d LOGPATH, --dir=LOGPATH
                            target dir for log file.
      -t INTERVAL, --interval=INTERVAL
                            monitor interval (seconds), default 5m
      -l LOOP, --loop=LOOP  monitor loop mode. default is: True

    This is a server monitor for CPU, Memory, Disk and support rest api

如每5秒监控服务器性能，并开启API服务

```python monitorRestApi.py -t 5```

打开 http://127.0.0.1:5000/ 查看接口和返回数据。