#!/usr/bin/python
#coding=utf-8

'''
Created on 2016-5-6
@author: Michael Yu
'''

import pycurl
import json
import StringIO
import time
import threading
import my_env

'''PostImpl
Wrapping Curl object
'''
class PostImpl(object):
    def __init__(self, url, data, token=None):
        super(PostImpl, self).__init__()
        
        self.c = pycurl.Curl()
        self.url = my_env.url_prefix + url;
        
        self.data = data
        if type(data) is type({}):
            self.data = json.dumps(data)
            
        self.buffer = StringIO.StringIO()
        
        self.headers = ["Content-Type: application/json; charset=utf-8", 
                        my_env.header_appid, 
                        my_env.header_appkey, 
                        "X-LC-Prod: 1"]
        
        self.token = None
        if token is not None:
            self.token = token
            self.headers.append(str("X-LC-Session: "+token))
        
        self._before_post()
        
    def __del__(self):
        self.buffer.close()
        
    def show_headers(self):
        print self.headers
    
    def _before_post(self):
        self.c.setopt(pycurl.SSL_VERIFYPEER, False)
        self.c.setopt(pycurl.HTTPHEADER, self.headers)
        self.c.setopt(pycurl.URL, self.url)
        self.c.setopt(pycurl.POSTFIELDS, self.data)
        self.c.setopt(pycurl.WRITEFUNCTION, self.buffer.write)
        self.c.setopt(pycurl.NOSIGNAL, 1)
    
    def post(self):
        self.c.perform()
        return self._after_post()
    
    def _after_post(self):
        response = self.buffer.getvalue()
        self.buffer.close()
        self.buffer = StringIO.StringIO()
        return response
    
class PostWithLoginImpl(object):
    def __init__(self, url, data, username, password):
        super(PostWithLoginImpl, self).__init__()
        
        self.username = username
        self.password = password
        self.login_post = PostImpl("/1.1/login", {"username":username,"password":password})
        self.post = PostImpl(url, data, self.get_token())
        
    def get_token(self):
        res = self.login_post.post()
        resjson = json.loads(res)
        return resjson['sessionToken']
    
class PostThread(threading.Thread):
    def __init__(self, post_impl, ev, lock, name=None):
        threading.Thread.__init__(self)
        self.post_impl = post_impl
        self.ev = ev
        self.lock = lock
        if name is not None:
            self.name = name
    
    def getResult(self):
        return (self.res, self.post_impl.c)
    
    def run(self):
        self.ev.wait()
        if self.lock.acquire():
            self.res = self.post_impl.post()
            print "%s - %s - %s" % (self.name, time.ctime(), self.res)
        self.lock.release()
    
if __name__=='__main__':
    pass
    