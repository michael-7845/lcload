#!/usr/bin/python
#coding=utf-8

'''
Created on 2016-5-12
@author: michael yu
'''

class MyDict(dict):
    def __getattr__(self,name):
        if name in self:
            return self[name]
        n=MyDict()
        super(MyDict, self).__setitem__(name, n)
        return n
    def __getitem__(self,name):
        if name not in self:
            super(MyDict, self).__setitem__(name,nicedict())
        return super(MyDict, self).__getitem__(name)
    def __setattr__(self,name,value):
        super(MyDict, self).__setitem__(name,value)

if __name__=="__main__":
    pass
    