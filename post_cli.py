#!/usr/bin/python
# -*- coding: utf-8 -*-  

'''
Created on 2016-5-11
@author: Michael Yu
'''

import sys
import os
import optparse

import loadtest
from post_config import LoadtestConfig

def commandui(args=sys.argv[1:]):
    parser = optparse.OptionParser(usage="%prog [options]", version="%prog 1.0")
    
    parser.add_option("-c", "--config",
                      dest="config",
                      action="store",
                      default="loadtest.ini",
                      help='loadtest tool config file. By default, loadtest.conf')
    parser.add_option("-w", "--waittime",
                      dest="waittime",
                      action="store",
                      default=5,
                      type="int",
                      help='gathering wait time before request. By default, 5s')
    
    (options, args) = parser.parse_args(args)
    
    config = LoadtestConfig(options.config)
    samplings = _data_from_config(config)
    for sampling in samplings:
        (casename, is_login, url, data) = sampling
        print "testing %s" % casename
        if is_login:
            _run(loadtest.multipost_afterlogin, url, data, options.waittime)
        else:
            _run(loadtest.multipost_nologin, url, data, options.waittime)
    
def _run(func, url, data, waittime):
    results = func(url, data)
    
    from post_report import ThreadResult
    r = []
    for res in results:
        t = ThreadResult(res[0], res[1])
#        t._show()
        r.append(t)
    
    from post_report import ThreadReport
    tr = ThreadReport(r)
    tr.report()
    
def _data_from_config(config):
    result = []
    cases = config.CASE
    for (case, mp) in cases.items():
        for v in mp.values:
            v['data'] = eval(v['data'])
        result.append((case, mp.is_login, mp.url, mp.values))
    return result
    
if __name__ == '__main__':
#    commandui(["-c", "loadtest_sample.conf"])
    commandui()
    