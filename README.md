# django2总结

 1. 项目地址(http://tools.ayjin.cn/)
 2. 部署问题
 3. django2和xadmin
 4. 常见问题及其解决方案

## 部署问题
1. 使用环境:
	1. 安装好xshell和xftp
	2. python==3.6.8
	2. 腾讯云ubuntu==18.04 ltsb
	3. mysql==8.0
	3. django==2.2
	4. nginx==1.14
	5. uwsgi==2.0.19
2. 安装教程
	1. 安装xshell和xftp
[软件链接](https://pan.baidu.com/s/12CwdpAPLtlrwabfW9E1cXQ)#提取码ajin
	2. 将服务器切换为root
		```
		$ sudo passwd root #然后设置密码
		$ sudo vim /etc/ssh/sshd_config #允许ssh连接root账号：找到PermitRootLogin 这项 将其改为 yes
		```
	3. 虚拟环境的配置
		```
		$ 在root权限下安装
		$ pip3 install virtualenv
		$ pip3 install virtualenvwrapper
		$ vim ~/.bashrc #将两个路径添加到文件里
		$ source ~/.bashrc #刷新配置文件
		```
		如果不知道怎么加[点这里](https://blog.csdn.net/weixin_40576643/article/details/80884135)
	4. mysql8.0的安装
		```
		$ wget https://dev.mysql.com/get/mysql-apt-config_0.8.10-1_all.deb #把deb包下载好
		$ sudo dpkg -i mysql-apt-config_0.8.10-1_all.deb #添加到软件源
		$ sudo apt-get update #更新软件源
		$ sudo apt-get install mysql-server #安装mysql
		$ pip3 install mycli #这是一个python的命令行提示sql语句工具，超级好用
		$ mycli -uroot -p #试试登录，一般没什么问题
		```
	5. 配置数据库远程连接
		首先我们登录root数据库账号，添加一个账号，方便远程使用。
		```
		$ use mysql;#一般mysql的配置都在这里。
		$ select user,host from user;#先看看有哪些账户，host如果为%,表示允许任何设备进行连接，如果为localhost表示只允许本地连接。
		$ create user ayjin@'%' identified  by 'password';#创建一个允许任何主机访问的账号ayjin，密码为password
		$ grant all privileges on *.* to ayjin@'%' with grant option;#这里为ayjin的用户添加了对所有数据库的所有权限，*.*表示所有数据库。
		$ flush privileges;#刷新权限。
		$ ALTER USER 'ayjin'@'%' IDENTIFIED WITH mysql_native_password BY 'password';#这一步可选可不选，如果出现远程连接不上，试试这个。修改远程连接用户的加密规则。
		$ mycli -u ayjin -p #试试登陆这个号，看看能不能查表。
		```
	   6. django2的安装
		```
		$ mkvirtualenv django22 #整个虚拟环境
		$ pip install django==2.2 #安装django2.2
		```
		下载xadmin2对应的版本[xadmindj2](https://github.com/sshwsfc/xadmin/tree/django2)
		```
		$ pip install -r requirements.txt #安装对应依赖。
		```
		常见的坑解决方案[解决方案](https://www.jianshu.com/p/3a3afda82f72)
	   7. nginx和uwsgi的安装
		```
		apt-get nginx #安装成功的话，直接打开浏览器输入ip，出现页面即可。
		apt-get uwsgi #
		```
		关于uwsgi[教程](https://www.runoob.com/python3/python-uwsgi.html)
		这里我只想说明一个点，在创建my_uwsgi.ini文件的时候，一定一定要在文件第一行**声明这是一个uwsgi文件**[uwsgi]，否则运行会报错！
	   8. 如果出现一个问题，通过uwsgi无法访问的话，记得检查一下安全组，常用的8080、8000端口这些都不是默认打开的，自己添加进去。

## django2理解
对于我来说，我目前的理解也仅仅是知道怎么用而已，这里就简要的说一下吧，参考这个[详细教程](https://www.runoob.com/django/django-tutorial.html)
这里我直接拿项目来进行解释。
![项目树形图](https://github.com/ay1Jin/website/blob/main/doc/img/tree.PNG)
- apps:如果app过多的话，可以整合到一个文件夹中。
- extra_apps:例如我们引入的xadmin就需要放到这里面
- mysite:里面存放了我们这个项目的基本文件
	- urls.py:配置路由
	- settings.py:配置文件
	- wsgi.py:和uwsgi部署时使用
- script:存放一些和项目没有关系的python脚本，比如更新爬虫数据库。
- statics:存放我们的静态文件
	- css
	- js
	- img
- templates:存放我们的html模板
- clientmanager:我们创建的app
- servermanager:我们创建的app

这里我主要讲一下app，我们的app是通过manage.py startapp name创建的，我们可以这么理解成一个app对应着数据库里的一张表。这里以servermanager的app为例
- servermanager
	- models.py 这里定义我们打算创建一个怎么样的数据表，它会同步到数据库中。
	- views.py 这里定义我们的页面操作，比如向页面传递什么参数、返回什么页面、等等。
	- adminx.py 这里定义我们的xadmin
	- apps.py 对我们这个app的一些基本信息的配置。
	- init.py 初始化这个app时我们的操作。

1. models.py

``` python
from django.db import models

# Create your models here.
class PicManage(models.Model):
    title = models.CharField('标题',max_length=100,default='图片.jpg')
    time = models.DateTimeField('上传时间',auto_now_add=True)
    path = models.CharField('路径',max_length=100)
    isShow = models.CharField('是否显示',max_length=1,choices=(('1','show'),
                                                    ('0','unshow')
                                                    ))
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = u'图片'#方便后台对我们这个数据表的别名
        verbose_name_plural = verbose_name
```
这里的话，我们就相当于在数据库中创建了一个servermanage_picmanage的数据表。
2. adminx.py

``` python
import xadmin
from servermanager.models import PicManage
from xadmin import views

class GlobalSettings(object):
    site_title = 'Aha?'#设置了后台标题名
    site_footer = "ayjin's website"#设置了后台底部名
    menu_style = 'accordion'#侧边栏是否可折叠
xadmin.site.register(views.CommAdminView,GlobalSettings)#把这个配置注册到xadmin中才会生效

class PicAdmin(object):
    list_display = ('title','time','path','isShow',)#后台管理中，显示的列
    search_fields = ('title',)#查询框，查询title
    model_icon = 'fa fa-camera-retro'#设置图标
    list_per_page = 10#设置每一页显示的列表数据数量
xadmin.site.register(PicManage,PicAdmin)#注册到xadmin中
```
3. apps.py

``` python
from django.apps import AppConfig


class ServermanagerConfig(AppConfig):
    name = 'servermanager'
    verbose_name = '内容管理'#侧边栏我们顶级标题称为内容管理。

```
4. init.py

``` python
default_app_config = 'servermanager.apps.ServermanagerConfig'
#使文件一开始就让我们的配置类文件生效
```
- clientmanager
	- views.py

1. views.py

``` python
from django.shortcuts import render,render_to_response,HttpResponse
from servermanager.models import PicManage
from django.core.paginator import Paginator#插入分页插件
# Create your views here.
def index(request):
    picMsgs = PicManage.objects.all()[:4]#查询数据库前四个数据
    return render_to_response('index.html',locals()) #locals()表示返回的这个函数中所有的变量。

def pictures(request,num=1):
    #获得全部数据库信息
    queryset = PicManage.objects.all()
    #设置每页12个
    paginator = Paginator(queryset,12)
    #总页数
    pageCount = paginator.num_pages
    #当前页面类
    pageInfo = paginator.get_page(num)
    return render_to_response('pictures.html',locals())


def picture(request,name,time,path):
    print(path)
    return render(request,'picture.html',{'ImgLink':path,'ImgName':name,'UploadTime':time})

def test(request,age,name,msg):
    print(age)
    print(name)
    print(msg)
    return HttpResponse(age,name)

def page_not_found(request,exception):
    return render(request,'404.html')
```

  
  



 
	
