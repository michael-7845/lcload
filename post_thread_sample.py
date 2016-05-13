#!/usr/bin/python
#coding=utf-8

'''
Created on 2016-5-10

@author: michael yu
'''

import time
import threading
import json

from post_thread import PostImpl, PostWithLoginImpl, PostThread

def demo_login_userinfo_in_PostImpl():
    login_post = PostImpl("/1.1/login", 
                            {"username":"user00001@may.event","password":"123456"})
    res = login_post.post()
    print res
    resjson = json.loads(res)
    print resjson['sessionToken']
    
    user_info_post = PostImpl("/1.1/functions/user_info", 
                                {"userId":"56c7d005d342d300543379e2"},
                                resjson['sessionToken'])
    user_info_post.show_headers()
    res = user_info_post.post()
    resjson = json.loads(res)
    print resjson
    
def demo_login_userinfo_in_PostWithLoginImpl():
    user_info_post = PostWithLoginImpl("/1.1/functions/user_info", 
                                        {"userId":"56c7d005d342d300543379e2"},
                                        "user00001@may.event",
                                        "123456")
    user_info_post.post.show_headers()
    res = user_info_post.post.post()
    resjson = json.loads(res)
    print resjson
    
def demo_postthread(n):
    e = threading.Event()
    threads = []
    locks = []
    for i in range(n):
        hello_post = PostImpl("/1.1/functions/hello", {})
        lock = threading.Lock()
        pthread = PostThread(hello_post, e, lock)
        threads.append(pthread)
        locks.append(lock)
        pthread.start()
    
    time.sleep(2)
    print "sending posts."
    e.set();
    
    for i in range(n):
        threads[i].join()
        
    for i in range(n):
        print threads[i].getResult()
        
def call_demo_userinfo_postthread():
    url = "/1.1/functions/user_info"
    data = ({"username":"user00001@may.event", 
             "password":"123456", 
             "data":{"userId":"56c7d005d342d300543379e2"}},
            {"username":"user00002@may.event", 
             "password":"123456", 
             "data":{"userId":"56c7d005d342d300543379e2"}},
            {"username":"user00003@may.event", 
             "password":"123456", 
             "data":{"userId":"56c7d005d342d300543379e2"}})
    
    demo_userinfo_postthread(url, data)
        
def demo_userinfo_postthread(url, data):
    print url
    for d in data:
        print d["username"], d["password"], d["data"]
        
    n = len(data)
    e = threading.Event()
    threads = []
    locks = []
    for i in range(n):
        api = PostWithLoginImpl(url, data[i]["data"], data[i]["username"], data[i]["password"])
        lock = threading.Lock()
        pthread = PostThread(api.post, e, lock)
        threads.append(pthread)
        locks.append(lock)
        pthread.start()
    
    time.sleep(2)
    print "sending posts."
    e.set();
    
    for i in range(n):
        threads[i].join()
        
    for i in range(n):
        print threads[i].getResult()
        
        
if __name__ == '__main__':
#    demo_login_userinfo_in_PostImpl()
#    demo_login_userinfo_in_PostWithLoginImpl()
#    demo_postthread(100)
    call_demo_userinfo_postthread()
    