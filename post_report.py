#!/usr/bin/python
# -*- coding:utf-8 -*-
'''
Created on 2016-5-11

@author: Michael Yu
'''

import json
import pycurl

class ThreadResult(object):
    def __init__(self, response, curl):
        self.response = response
        self.curl = curl
        
        self._prepare()
        
    def _prepare(self):
        self.res_in_json = json.loads(self.response)
        self.namelookup_time = self.curl.getinfo(pycurl.NAMELOOKUP_TIME) # 域名解析时间
        self.connect_time = self.curl.getinfo(pycurl.CONNECT_TIME) # 远程服务器连接时间
        self.pretransfer_time = self.curl.getinfo(pycurl.PRETRANSFER_TIME) # 连接上后到开始传输时的时间
        self.starttransfer_time = self.curl.getinfo(pycurl.STARTTRANSFER_TIME) # 接收到第一个字节的时间
        self.total_time = self.curl.getinfo(pycurl.TOTAL_TIME) # 上一请求总的时间
        self.redirect_time = self.curl.getinfo(pycurl.REDIRECT_TIME) # 如果存在转向的话，花费的时间
        self.http_code = self.curl.getinfo(pycurl.HTTP_CODE) # HTTP响应代码
        self.response_code = self.curl.getinfo(pycurl.RESPONSE_CODE) # 响应代码
        self.redirect_count = self.curl.getinfo(pycurl.REDIRECT_COUNT) # 重定向的次数
        self.size_upload = self.curl.getinfo(pycurl.SIZE_UPLOAD) # 上传的数据大小
        self.size_download = self.curl.getinfo(pycurl.SIZE_DOWNLOAD) # 下载的数据大小
        self.speed_upload = self.curl.getinfo(pycurl.SPEED_UPLOAD) # 上传速度
        self.speed_download = self.curl.getinfo(pycurl.SPEED_DOWNLOAD) # 下载速度
        self.header_size = self.curl.getinfo(pycurl.HEADER_SIZE) # 头部大小
        self.request_size = self.curl.getinfo(pycurl.REQUEST_SIZE) # 请求大小
        
    def _show(self):
        self._prepare()
        print '''result id: %s, 
域名解析时间: %s, 
远程服务器连接时间: %s, 
连接上后到开始传输时的时间: %s, 
开始传输和接收的时间: %s, 
请求总的时间: %s, 
转向花费的时间: %s, 
HTTP响应代码: %s, 
响应代码: %s, 
重定向的次数: %s, 
上传的数据大小: %s, 
下载的数据大小: %s, 
上传速度: %s, 
下载速度: %s, 
头部大小: %s, 
请求大小: %s 
''' % (id(self), self.namelookup_time, self.connect_time, self.pretransfer_time, \
       self.starttransfer_time, self.total_time, self.redirect_time, \
       self.http_code, self.response_code, self.redirect_count, \
       self.size_upload, self.size_download, self.speed_upload, \
       self.speed_download, self.header_size, self.request_size)
        
class ThreadReport():
    def __init__(self, results):
        self.results = results
        
    def _total_time_average(self):
        _sum = 0; _count = 0
        for res in self.results:
            _sum += res.total_time
            _count += 1
        return _sum/_count
    
    def _code_not_200_rate(self):
        _sum = 0; _count = 0
        for res in self.results:
            _count += 1
            if res.http_code != 200:
                _sum += 1
        return _sum/_count
    
    def _namelookup_time_average(self):
        _sum = 0; _count = 0
        for res in self.results:
            _sum += res.namelookup_time
            _count += 1
        return _sum/_count
    
    def _connect_time_average(self):
        _sum = 0; _count = 0
        for res in self.results:
            _sum += res.connect_time
            _count += 1
        return _sum/_count
    
    def report(self):
        _format = '''平均请求耗时: %f,
非成功200响应的比率: %f
平均域名解析时间: %f,
平均服务器连接时间: %f 
'''
        print _format % (self._total_time_average(), 
                         self._code_not_200_rate(), 
                         self._namelookup_time_average(), 
                         self._connect_time_average())
        
if __name__ == '__main__':
    pass