# -*- coding:utf-8 -*-
# date 2018/4/24
# author birthpla
import requests
import lxml
from bs4 import BeautifulSoup
from spider_company1 import Spider

class com_spider(object):
    def __init__(self):
        self.headers={
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"zh-CN,zh;q=0.9",
            "Cache-Control":"max-age=0",
            "Connection":"keep-alive",
            "Host":"b2b.huangye88.com",
            "Upgrade-Insecure-Requests":"1",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36"
        }
        self.spider = Spider()

    def get_hangye(self):
        hangye=[]
        html = requests.get("http://b2b.huangye88.com/jiangsu", headers=self.headers).text
        beautifulsoup = BeautifulSoup(html,'lxml')
        tag_list = beautifulsoup.find_all('div',attrs={'class':'tag_tx'})
        for l in tag_list:
            hangye_list = l.find_all('li')
            for hy in hangye_list:
                hangye.append(hy.find('a').get('href'))
        print(hangye)
        return hangye

    def get_allcom_by_hhuangye(self):
        hangye = self.get_hangye()
        for hy in hangye:
            i=1
            while(1):
                allcom = []
                try:
                    url = hy + "pn{}".format(i)
                    print(url)
                    html = requests.get(url, headers=self.headers).text
                    beautifulsoup = BeautifulSoup(html, 'lxml')
                    form = beautifulsoup.find(name='div', attrs={'class': 'mach_list2'}).find('form').find_all('dl')
                    for com in form:
                        try:
                            name = com.find('dt').find('h4').text
                            allcom.append(name)
                        except Exception as e:
                            pass
                    i = i + 1
                except Exception as e:
                    print("获取该行业公司名录完毕")
                    break
                print(allcom)
                print('即将进入国家企业信用网站爬取....')
                try:
                    self.spider.get_all(allcom)
                except Exception as e:
                    print('获取该行业完毕')
                    break

    def get_allcom_by_txt(self,filename):
        file = open(filename,'r',encoding='utf-8')
        lines = file.readlines()
        self.spider.get_all(lines)
        file.close()



if __name__ == '__main__':
    spider = com_spider()
    spider.get_allcom_by_txt('F:\python\公司名录\江苏.txt')