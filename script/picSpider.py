# c
#__author:ayjin
#__Date:2020-11-15
#__Orginazation:JLUZH
#__Topic:The pic spider of the:http://www.obzhi.com/

import os
import requests
import re
import multiprocessing
from lxml import etree

# 请求头添加
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0'
}

# 注意这里最好检查一下域名结尾有没有更改，有更改在这里进行修改即可。
SpiderList = [
    'dongmanbizi',
    'lingleibizhi',
    'jianyuebizhi',
    'fengjingbizhi',
    'renwubizhi',
    'youxibizhi',
    'shoujibizhi',
    'yuanchuangchahua',
    'dongwubizhi',
    'qqtouxiang',
]


# 为每个分类列表创建文件夹,注意先要自己创建一个文件夹img
def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
        # print('创建新文件夹:',path)

    else:
        # print('已存在文件夹:',path)
        pass


# 构建了爬虫分类列表链接 http://www.obzhi.com/category/dongmanbizi
Domain = 'http://www.obzhi.com/category/'
SpiderUrl = []
for l in SpiderList:
    url = Domain + l
    SpiderUrl.append(url)
    path = './img/' + l
    mkdir(path)


# 下载图片(单独写这个函数是方便多进程)
def DownloadImg(name, path, src):
    img = gethtml(src)
    with open(path, 'wb') as f:
        f.write(img)
        f.close()
    print('图片：' + name + ' 链接:' + src + '下载已经完成!')

def gethtml(url):
    i = 0
    while i < 3:
        try:
            html = requests.get(url,timeout=5).content
            return html
        except requests.exceptions.RequestException:
            print('重连中')
            i+=1

def gettext(url):
    i = 0
    while i < 3:
        try:
            html = requests.get(url,timeout=5).content
            return html
        except requests.exceptions.RequestException:
            i+=1
if __name__ == "__main__":
    # 这里不指定进程池数量，默认使用电脑CPU核数进行爬取，鲁棒性较强。
    p = multiprocessing.Pool()
    # 遍历分类
    for i in range(0, len(SpiderList)):
        Type = SpiderList[i]  # 每个分类dongmanbizi
        url = SpiderUrl[i]  # 每个分类的链接http://www.obzhi.com/category/dongmanbizi
        # print(Type+':'+url)#dongmanbizi:http://www.obzhi.com/category/dongmanbizi
        # 得到当前分类的最后一页
        response = gettext(url)
        responseHtml = etree.HTML(response)
        pagination = responseHtml.xpath('//div[@class="navigation container"]//a[@class="extend"]/@href')
        # 加入判断防止抓取不到最后一页
        if len(pagination) > 0:
            EndPage = pagination[0].split('/')[-1]
            # print('当前类型:' + Type + '的最后一页为:' + str(EndPage))
        else:
            EndPage = 1
        pat = 'src=(.*?)&'
        print(Type + ':' + url + '共' + str(EndPage) + '页')
        # print(EndPage)
        # 遍历每一页
        for i in range(1, int(EndPage) + 1):
            # 获得当前页面的图片链接#http://www.obzhi.com/3856.html
            # print('当前页面：',i)
            PageUrl = url + '/page/' + str(i)
            response = gettext(PageUrl)
            responseHtml = etree.HTML(response)
            src = responseHtml.xpath('//div[@class="mainleft"]/ul//li/div[@class="thumbnail"]/a/img/@src')
            texts = responseHtml.xpath('//div[@class="mainleft"]/ul//li/div[@class="article"]/h2//text()')
            for i in range(0, len(src)):
                rst = re.compile(pat).findall(src[i])
                # print(texts[i]+':'+rst[0])
                path = './img/' + Type + '/' + texts[i] + '.jpg'
                s = rst[0]
                p.apply_async(DownloadImg, args=(texts[i], path, s,))

    p.close()
    p.join()
    print('All pic is be Download~')