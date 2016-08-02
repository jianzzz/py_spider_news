# coding=utf-8
__author__ = 'zhuangjian'

import urllib
import http.cookiejar
import re
import os,sys
import time
import requests
class Spider:

    def __init__(self):
        if len(sys.argv)>1:
            self.dir = sys.argv[1]+"/news"
        else:
            self.dir = "news"
        self.baidu_SiteURL = 'http://news.baidu.com/'
        self.fenghuang_SiteURL = 'http://news.ifeng.com/'
        self.weibo_SiteURL = 'http://d.weibo.com/100803_-_page_hot_list?cfs=&Pl_Discover_Pt6Rank__5_filter=hothtlist_type%3D1#_0'

        self.xiguaji_Entry_SiteUrl = "http://www.xiguaji.com/Login"
        self.xigua_Login_SiteURL = 'http://www.xiguaji.com/Login/Login'
        self.xigua_Qiche_SiteURL = 'http://www.xiguaji.com/MArticleCollect/PopularArticle/?tagId=28&dateCode=0&partial=1'
        self.xigua_Keji_SiteURL = 'http://www.xiguaji.com/MArticleCollect/PopularArticle/?tagId=30&dateCode=0&partial=1'

    def getPage(self,siteURL,decode):
        request = urllib.request.Request(siteURL)
        request.add_header('User-agent', 'spider')#新浪有反爬虫，可以设置一下User-Agent，把自己伪装成搜索引擎爬虫，谷歌、必应都可以，或者仅仅用spider也行！
        response = urllib.request.urlopen(request)
        return response.read().decode(decode)

    def baidu_getContents(self):
        contents = []
        page = self.getPage(self.baidu_SiteURL,"gbk")
        #热点要闻
        '''
        pattern = re.compile('<div.*?id="body".*?<div.*?id="focus-top".*?<div.*?id="pane-news".*?>(.*?)</div>(.*?)</div>', re.S)
        pane_news = re.findall(pattern, page)
        pattern = re.compile('<div.*?alog-group="focustop-hotnews".*?<ul.*?>(.*?)</ul>', re.S)
        hot_news = re.findall(pattern, pane_news[0][0])
        pattern = re.compile('<li.*?<strong>.*?<a.*?>(.*?)</a>', re.S)
        names = re.findall(pattern, hot_news[0])
        for name in names:
            contents.append(name)

        pattern = re.compile('<ul.*?class="ulist focuslistnews".*?<li.*?<span class="dot".*?</span>.*?<a.*?>(.*?)</a>', re.S)
        focuslist_news = re.findall(pattern, pane_news[0][1])
        for name in focuslist_news:
            contents.append(name)
        '''
        #热搜新闻词
        pattern = re.compile('<div.*?id="body".*?<div.*?id="focus-top".*?<div.*?class="l-right-col".*?<div.*?alog-group="focus-top-news-hotwords".*?<div.*?class="bd".*?<ul.*?class="hotwords clearfix".*?>(.*?)</ul>', re.S)
        hot_words = re.findall(pattern, page)
        pattern = re.compile('<li.*?<a.*?>(.*?)</a>', re.S)
        names = re.findall(pattern, hot_words[0])
        for name in names:
            name = name.replace('<br/>','').replace('#','').replace('\t','').replace('\n','').replace(' ','')
            print (name)
            contents.append(name)
        return contents

    def fenghuang_getContents(self):
        contents = []
        page = self.getPage(self.fenghuang_SiteURL,'utf-8')

        #pattern = re.compile('<div.*?id="box01".*?<div.*?class="clearfix".*?<div.*?class="col_left".*?'+
         #                    '<div.*?class="left_co1".*?>(.*?)<div.*?class="tit1 clearfix">',re.S)
        pattern = re.compile('<div.*?class="left_co1".*?>(.*?)<div class="tit1 clearfix">',re.S)
        tit = re.findall(pattern, page)
        pattern = re.compile('<a.*?>(.*?)</a>', re.S)
        names = re.findall(pattern, tit[0])
        for name in names:
            name = name.replace('<br/>','').replace('#','').replace('\t','').replace('\n','').replace(' ','')
            print (name)
            contents.append(name)
        return contents

    def weibo_getContents(self):
        contents = []
        page = self.getPage(self.weibo_SiteURL, 'utf-8')

        pattern = re.compile('<div.*?id="Pl_Discover_Pt6Rank__5".*?>(.*?)<div class="WB_main_r">', re.S)
        m_wrap = re.findall(pattern, page)
        pattern = re.compile('<div.*?class="m_wrap clearfix".*?<ul.*?class="pt_ul clearfix".*?>'
                             '(.*?)</ul>', re.S)
        pt_li = re.findall(pattern, m_wrap[0])
        pattern = re.compile('<div.*?class="title W_autocut".*?<span.*?</span>.*?<a.*?>(.*?)</a>', re.S)
        names = re.findall(pattern, pt_li[0])
        for name in names:
            name = name.replace('<br/>','').replace('#','').replace('\t','').replace('\n','').replace(' ','')
            print (name)
            contents.append(name)
        return contents

    def xigua_auto_login(self,email, pwd):
        s = requests.Session()
        r = s.get(self.xiguaji_Entry_SiteUrl)#首先获取登录界面，session自动记录cookie
        pattern = re.compile("chk:'(.*?)'",re.S)
        chk = re.findall(pattern, r.text)
        postData =  {
            'email': email,
            'password': pwd,
            'chk': chk[0],  #登录参数 chk 由模版生成，会和 cookieSession 校验，需要动态设置
            'validateCode': ''}
        # 注意，s.post使用的data不需要编码，直接传json即可
        r = s.post(self.xigua_Login_SiteURL,postData)#第二次调用，进行账号密码校验
        print (r.content.decode("utf-8"))
        return s

    def xigua_getContents(self,session,url):
        contents = []
        page = session.get(url).content.decode("utf-8")
        pattern = re.compile('<tr.*?<td.*?<a.*?>(.*?)</a>', re.S)
        names = re.findall(pattern, page)
        for name in names:
            name = name.replace('<br/>','').replace('#','').replace('\t','').replace('\n','').replace(' ','')
            print(name)
            contents.append(name)
        return contents

    def saveFile(self, content,dir, name):
        fileName = dir+"/"+name + ".txt"
        f = open(fileName, "a+")
        for c in content:
            f.writelines(c)
            f.writelines('\r\n')
        f.close()

    def mkdir(self,path):
        path = path.strip()
        isExists=os.path.exists(path)
        if not isExists:
            os.makedirs(path)
            return True
        else:
            return False

    def saveInfo(self):
        self.mkdir(self.dir)
        fileName = "news_"+time.strftime('%Y-%m-%d_%H_%M_%S')

        print ("spider 百度新闻...")
        contents = self.baidu_getContents()
        contents.insert(0,"From 百度新闻:\n")
        contents.append("\n")
        self.saveFile(contents,self.dir,fileName)

        print ("spider 凤凰资讯...")
        contents = self.fenghuang_getContents()
        contents.insert(0,"From 凤凰资讯:\n")
        contents.append("\n")
        self.saveFile(contents,self.dir,fileName)

        print ("spider 新浪微博发现...")
        contents = self.weibo_getContents()
        contents.insert(0,"From 新浪微博发现:\n")
        contents.append("\n")
        self.saveFile(contents,self.dir,fileName)

        print("spider 西瓜汽车...")
        session = self.xigua_auto_login("email","password") #这里需要添加你自己的邮箱和密码
        contents = self.xigua_getContents(session,self.xigua_Qiche_SiteURL)
        contents.insert(0,"From 西瓜汽车:\n")
        contents.append("\n")
        self.saveFile(contents,self.dir,fileName)

        print("spider 西瓜科技...")
        contents = self.xigua_getContents(session,self.xigua_Keji_SiteURL)
        contents.insert(0,"From 西瓜科技:\n")
        contents.append("\n")
        self.saveFile(contents,self.dir,fileName)

spider = Spider()
spider.saveInfo()
