#!/usr/bin/python
# *-* coding=utf-8 *-*

'''
Created on 2016-5-11

@author: admin
'''
    
import ConfigParser
import my_dict
    
def _read_config(config_file):
    cf = ConfigParser.ConfigParser()
    cf.read(config_file)
    secs = cf.sections()
    d = {}
    for sec in secs:
        d[sec] = {}
        opts = cf.options(sec)
        for opt in opts:
            if opt.startswith(r"is_"):
                d[sec][opt] = cf.getboolean(sec, opt)
            elif opt.startswith(r"i_"):
                d[sec][opt] = cf.getint(sec, opt)
            elif opt.startswith(r"f_"):
                d[sec][opt] = cf.getfloat(sec, opt)
            else:
                d[sec][opt] = cf.get(sec, opt)
    return d
    
class Section(object):
    def __init__(self, options):
        for (k, v) in options.items():
            setattr(self, k, v)

class Config:
    def __init__(self, sections):
        for (k, v) in sections.items():
            s = Section(v)
            setattr(self, k, s)
    
class LoadtestConfig(object):
    _structure = {"case_":("url", "file", "is_login"),
                  "setting":("i_mode", )}
    
    def __init__(self, file_path):
        self.file_path = file_path
        self.config = LoadtestConfig._get_config(self.file_path)
        self._parse()
        
    @classmethod
    def _get_config(cls, file_path):
        import os
        if not os.path.exists(os.path.join(os.getcwd(), file_path)):
            print "%s does not exist!" % os.path.join(os.getcwd(), file_path)
            exit(1)
        config = Config(_read_config(file_path))
        return config
    
    def _parse(self):
        self._CASES = my_dict.MyDict()
        self._ONCE = my_dict.MyDict()
        for sec in vars(self.config):
            for (sec_prefix, key_attrs) in self._structure.items():
                if (sec.startswith(sec_prefix)): 
                    section = getattr(self.config, sec)
                    d = my_dict.MyDict()
                    
                    for attr in key_attrs:
                        if not hasattr(section, attr):
                            print "in [%s] section, no %s option!" % (sec, attr)
                            exit(1)
                        v = getattr(section, attr)
                        d[attr] = getattr(section, attr)
                    if sec.startswith("case_"):
                        self._CASES[sec] = d
                    elif sec.startswith("setting"):
                        self._ONCE[sec] = d
        
        self.ONCE = self._ONCE
        self.__make_params()
        
        return self._CASES
    
    def __make_params(self): # file in case_x
        s_params = my_dict.MyDict()
        m_params = my_dict.MyDict()
        
        for (name, v) in self._CASES.items():
            if (v.i_type == 0):
                s = SingleParameter(name, v.file, v.i_mode, v.i_type)
                s_params[name] = s
            elif True: # (v.i_type == 1): currently only use the multiple parameter type
                m = MultipleParameter(name, v.file, v.i_mode, v.i_type, v.url, v.is_login)
                m_params[name] = m
            else:
                print "parameter %s has an invalid type." % name
                exit(1)
                
        self.S = s_params
        self.M = self.CASE = m_params
    
class Parameter(object):
    def __init__(self, name, file, mode, type):
        self.name = name
        self.file = file
        self.mode = 0 # mode 0. currently only user the unique mode
        self.type = 1 # type 1. currently only user the multiple parameter type
    
    @classmethod
    def _read_many(cls, filepath):
        import os
        if not os.path.exists(filepath):
            print "%s does not exist!" % filepath
            exit(1)
        
        f = open(filepath, "r")
        data = [line.strip() for line in f.readlines() if len(line) > 0]
        f.close()
        while '' in data:
            data.remove('')
        return data
    
    def _unique_gen(self):
        for (i,v) in enumerate(self.values):
            yield v
    
    def _cycle_gen(self):
        size = len(self.values)
        index = -1;
        while (1):
            index += 1; n = index%size
            yield self.values[n]
            
    def gen(self):
        if self.mode == 0:
            return self._unique_gen()
        elif self.mode == 1:
            return self._cycle_gen()
        else:
            return None
    
class SingleParameter(Parameter):
    def __init__(self, name, file, mode, type):
        super(SingleParameter, self).__init__(name, file, mode, type)
        self._VALUES = self._read_many(file)[1:]
        self.values = self._VALUES
    
class MultipleParameter(Parameter): # case_x
    def __init__(self, name, file, mode, type, url='', is_login=False):
        super(MultipleParameter, self).__init__(name, file, mode, type)
        self.url = url
        self.is_login = is_login
        f = self._read_many(self.file)
        self._HEADER = f[0]
        self._VALUES = f[1:]
        self.values, self.size = self._parse_value(self._HEADER, self._VALUES)
    
    @classmethod
    def _parse_value(cls, _header, _values):
        header = [h.strip() for h in _header.strip().split(",")]
        headers_size = len(header)
        result = []
        for v in _values:
            value = [_v.strip() for _v in v.strip().split(",")]
            if headers_size != len(value):
                print "value number is not equal to parameter number!"
                exit(1)
            d = my_dict.MyDict()
            for i in range(headers_size):
                d[header[i]] = value[i]
            result.append(d)
        return result, len(result)
    
def demo():
    c = LoadtestConfig("loadtest_sample.conf")
    
    print c._CASES
    print c.CASE
    print c.CASE.case_1
    print c.CASE.case_2
    print c.CASE.case_1.name
    print c.CASE.case_1.values
    print c.CASE.case_1.size
    print c.CASE.case_1.url
    print c.CASE.case_1.is_login
    print c.CASE.case_2.values
    print c.CASE.case_2.is_login
    print c.ONCE.setting.i_mode
#    case1_gen = c.CASE.case_1.gen()
#    for i in range(3):
#        entry = case1_gen.next()
#        print entry.username
#        print entry.password
#        print entry.data
    
if __name__ == '__main__':
    demo()
    