爬虫百度新闻、凤凰资讯、新浪微博发现、西瓜公众号助手汽车和科技栏目
部分新闻关键字

需要注意的是西瓜公众号部分需要登录验证，且其登录参数 chk 由模版生成，会和 cookieSession 校验，需要动态设置，使用python requests的session用以确保cookie
唯一性

python 的 requests模块安装方式见 http://docs.python-requests.org/en/master/user/install/#get-the-source-code，安装后 IDE 记得重启。

本代码使用pyinstall打包为exe文件，方式见下：
windows:
http://pyinstaller.readthedocs.io/en/stable/requirements.html#windows

1、安装python，将安装路径写入path

2、根据python的版本和位数，下载pywin32(pyinstaller依赖)，https://sourceforge.net/projects/pywin32/files/pywin32/，执行安装

3、下载PyInstaller，github搜一个即可，解压

4、进入PyInstaller解压文件夹，执行python setup.py install安装PyInstaller

5、python pyinstaller.py 目标.py
如：python pyinstaller.py demo/spider_news.py
将在PyInstaller解压文件夹下生成对应目录
