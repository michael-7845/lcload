
1. 前提条件

* 推荐使用Ubuntu环境运行脚本

    Python 2.7 已经安装

* Ubuntu一般缺省已经安装Python

* pycurl已经安装

2. 工具脚本

* 发布地址

https://github.com/michael-7845/lcload
 
* 获取

$ git clone https://github.com/michael-7845/lcload.git
* 使用前
由于是公共git库 我把环境相关的重要信息: appkey appid appmasterkey 已经去掉, 请使用前在MyEnv.py中填写  
在执行前赋予脚本执行权限 chmod 774 *.py  

3. 使用

Usage: post_cli.py [options]
 
Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -c CONFIG, --config=CONFIG
                        loadtest tool config file. By default, loadtest.conf
  -w WAITTIME, --waittime=WAITTIME
                        gathering wait time before request. By default, 5s
                        