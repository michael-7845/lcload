#!/usr/bin/python
# -*- encode:utf-8 -*-
'''
Created on 2016-5-11

@author: Michael Yu
'''

import threading
import time

from post_thread import PostImpl, PostWithLoginImpl, PostThread

def multipost_afterlogin(url, data, waittime=5):
    '''Return post response result: list.
Send the https post request, using url and data.
After <waittime> seconds, send the post requests.
>>> url = "/1.1/functions/user_info"
>>> data = ({"username":"user00001@may.event", 
             "password":"123456", 
             "data":{"userId":"56c7d005d342d300543379e2"}},
            {"username":"user00002@may.event", 
             "password":"123456", 
             "data":{"userId":"56c7d005d342d300543379e2"}},
            {"username":"user00003@may.event", 
             "password":"123456", 
             "data":{"userId":"56c7d005d342d300543379e2"}})
>>> multipost_afterlogin(url, data)
>>> 
'''
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
    
    time.sleep(waittime)
    print "sending posts ..."
    e.set();
    
    for i in range(n):
        threads[i].join()
        
    result = []
    for i in range(n):
        result.append(threads[i].getResult())
    return result
    
def _demo_afterlogin():
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
    
    results = multipost_afterlogin(url, data)
    
    for res in results:
        print res[0]
        print res[1]
    print len(results)
    
    from post_report import ThreadResult
    for res in results:
        t = ThreadResult(res[0], res[1])
        t._show()
    
def multipost_nologin(url, data, waittime=5):
    '''Return post response result: list.
Send the https post request, using url and data.
After <waittime> seconds, send the post requests.
>>> url = "/1.1/functions/hello
>>> data = ({"data":{}},{"data":{}},{"data":{}})
>>> multipost_nologin(url, data)
>>> 
'''
    n = len(data)
    e = threading.Event()
    threads = []
    locks = []
    for i in range(n):
        api = PostImpl(url, data[i]["data"])
        lock = threading.Lock()
        pthread = PostThread(api, e, lock)
        threads.append(pthread)
        locks.append(lock)
        pthread.start()
    
    time.sleep(waittime)
    print "sending posts ..."
    e.set();
    
    for i in range(n):
        threads[i].join()
        
    result = []
    for i in range(n):
        result.append(threads[i].getResult())
    return result
    
def _demo_nologin():
    url = "/1.1/functions/hello"
    data = ({"data":{}},
            {"data":{}},
            {"data":{}})
    
    results = multipost_nologin(url, data)
    
    for res in results:
        print res[0]
        print res[1]
    print len(results)
    
    from post_report import ThreadResult
    r = []
    for res in results:
        t = ThreadResult(res[0], res[1])
        t._show()
        r.append(t)
    
    from post_report import ThreadReport
    tr = ThreadReport(r)
    tr.report()
    
if __name__ == '__main__':
#    _demo_afterlogin()
    _demo_nologin()
    