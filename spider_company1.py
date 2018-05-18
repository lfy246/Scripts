# -*-coding:utf-8 -*-
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from urllib.request import urlretrieve
from selenium import webdriver
from bs4 import BeautifulSoup
import PIL.Image as image
import requests
from Save import save_data
from bs4 import BeautifulSoup
import numpy as np
import random
import time
import re
import cv2


class Spider():
    def __init__(self):
        self.url = 'http://www.jsgsj.gov.cn:58888/province/'
        self.sql = save_data("company")
        self.browser = webdriver.Chrome('F:\\python\chromedriver.exe')
        self.wait = WebDriverWait(self.browser, 100)
        self.BORDER = 6
        self.headers={
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control":"max-age=0",
            "Connection": "keep-alive",
            "Host":"www.jsgsj.gov.cn:58888",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36"
        }


    def search(self,key):
        self.browser.refresh()
        keyword = self.wait.until(EC.presence_of_element_located((By.ID, 'name')))
        bowton = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'bt-chaxun')))
        keyword.send_keys(key)
        bowton.click()

    def get_images(self, bg_filename='bg.jpg', fullbg_filename='fullbg.jpg'):
        """
        获取验证码图片
        :return: 图片的location信息
        """
        bg = []
        fullgb = []
        while bg == [] and fullgb == []:
            bf = BeautifulSoup(self.browser.page_source, 'lxml')
            bg = bf.find_all('div', class_='gt_cut_bg_slice')
            fullgb = bf.find_all('div', class_='gt_cut_fullbg_slice')
        bg_url = re.findall('url\(\"(.*)\"\);', bg[0].get('style'))[0].replace('webp', 'jpg')
        fullgb_url = re.findall('url\(\"(.*)\"\);', fullgb[0].get('style'))[0].replace('webp', 'jpg')
        bg_location_list = []
        fullbg_location_list = []
        for each_bg in bg:
            location = {}
            location['x'] = int(re.findall('background-position: (.*)px (.*)px;', each_bg.get('style'))[0][0])
            location['y'] = int(re.findall('background-position: (.*)px (.*)px;', each_bg.get('style'))[0][1])
            bg_location_list.append(location)
        for each_fullgb in fullgb:
            location = {}
            location['x'] = int(re.findall('background-position: (.*)px (.*)px;', each_fullgb.get('style'))[0][0])
            location['y'] = int(re.findall('background-position: (.*)px (.*)px;', each_fullgb.get('style'))[0][1])
            fullbg_location_list.append(location)

        urlretrieve(url=bg_url, filename=bg_filename)
        print('缺口图片下载完成')
        urlretrieve(url=fullgb_url, filename=fullbg_filename)
        print('背景图片下载完成')
        return bg_location_list, fullbg_location_list

    def get_merge_image(self, filename, location_list):
        """
        根据位置对图片进行合并还原
        :filename:图片
        :location_list:图片位置
        """
        im = image.open(filename)
        new_im = image.new('RGB', (260, 116))
        im_list_upper = []
        im_list_down = []

        for location in location_list:
            if location['y'] == -58:
                im_list_upper.append(im.crop((abs(location['x']), 58, abs(location['x']) + 10, 166)))
            if location['y'] == 0:
                im_list_down.append(im.crop((abs(location['x']), 0, abs(location['x']) + 10, 58)))

        new_im = image.new('RGB', (260, 116))

        x_offset = 0
        for im in im_list_upper:
            new_im.paste(im, (x_offset, 0))
            x_offset += im.size[0]

        x_offset = 0
        for im in im_list_down:
            new_im.paste(im, (x_offset, 58))
            x_offset += im.size[0]

        new_im.save(filename)

        return new_im


    def is_pixel_equal(self, img1, img2, x, y):
        """
        判断两个像素是否相同
        :param image1: 图片1
        :param image2: 图片2
        :param x: 位置x
        :param y: 位置y
        :return: 像素是否相同
        """
        # 取两个图片的像素点
        pix1 = img1.load()[x, y]
        pix2 = img2.load()[x, y]
        threshold = 60
        if (abs(pix1[0] - pix2[0] < threshold) and abs(pix1[1] - pix2[1] < threshold) and abs(
                pix1[2] - pix2[2] < threshold)):
            return True
        else:
            return False

    def get_gap(self, img1, img2):
        """
        获取缺口偏移量
        :param img1: 不带缺口图片
        :param img2: 带缺口图片
        :return:
        """
        left = 43
        for i in range(left, img1.size[0]):
            for j in range(img1.size[1]):
                if not self.is_pixel_equal(img1, img2, i, j):
                    left = i
                    return left
        return left

    # 拖动函数
    def ease_out_expo(self, x):
            if x == 1:
                return 1
            else:
                return 1 - pow(2, -10 * x)

    def get_track(self, distance,seconds):
        tracks = [0]
        offsets = [0]
        for t in np.arange(0.0, seconds, 0.1):
            offset = self.ease_out_expo(t/seconds) * distance
            tracks.append(offset - offsets[-1])
            offsets.append(offset)
        sum = 0
        for i in tracks:
            sum = sum + i
        print(sum)
        return tracks

    def get_slider(self):
        """
        获取滑块
        :return: 滑块对象
        """
        while True:
            try:
                slider = self.browser.find_element_by_xpath("//div[@class='gt_slider_knob gt_show']")
                break
            except:
                time.sleep(0.5)
        return slider



    def move_to_gap(self, slider, track):
        """
        拖动滑块到缺口处
        :param slider: 滑块
        :param track: 轨迹
        :return:
        """
        ActionChains(self.browser).click_and_hold(slider).perform()
        for i in track:
            if(i-int(i)>0.5):
                i = i + 1
            else:
                pass
            ActionChains(self.browser).move_by_offset(xoffset=i, yoffset=0).perform()
        time.sleep(0.5)
        ActionChains(self.browser).release().perform()

    def crack(self,name):
        print("尝试验证5次")
        self.browser.switch_to_window(self.browser.window_handles[0])
        self.browser.get(self.url)
        for i in range(5):    #尝试验证5次
            # 打开浏览器并搜索
            self.search(name)

            # 保存的图片名字
            bg_filename = 'bg.jpg'
            fullbg_filename = 'fullbg.jpg'

            # 获取图片
            bg_location_list, fullbg_location_list = self.get_images(bg_filename, fullbg_filename)

            # 根据位置对图片进行合并还原
            bg_img = self.get_merge_image(bg_filename, bg_location_list)
            fullbg_img = self.get_merge_image(fullbg_filename, fullbg_location_list)

            # 获取缺口位置
            gap = self.get_gap(fullbg_img, bg_img)
            print('缺口位置', gap)

            track = self.get_track(gap - self.BORDER, 6)
            print('滑动滑块')
            print(track)
            # 点按呼出缺口
            slider = self.get_slider()
            time.sleep(2)
            # 拖动滑块到缺口处
            self.move_to_gap(slider, track)
            time.sleep(1)
            if (self.browser.current_url != self.url):
                print("验证成功")
                return
            else:
                print("验证失败")
                pass
            if(i==4):
                raise RuntimeError('五次验证失败，终止验证...')



    def get_all(self,name_lists):
        had_name = self.sql.get_hadcom('esta')
        for name in name_lists:
            if name in had_name:
                continue
            try:
                self.crack(name)
            except Exception as e:
                print("验证出错")
                continue
            time.sleep(2)
            page_list = self.browser.find_element_by_id("paginationzt").find_elements_by_tag_name('li')
            com_list = []
            for page in page_list[2:-2]:
                listboxes = self.browser.find_elements_by_class_name('listbox')
                for box in listboxes:
                    print(box.text)
                    if (box.find_element_by_class_name("status").find_elements_by_tag_name('p')[0].text != "在业"):
                        break
                    url = box.find_element_by_tag_name('a').get_attribute('href')
                    com_list.append(url)
                js = "var q=document.documentElement.scrollTop=800"
                self.browser.execute_script(js)
                time.sleep(1)
                self.browser.find_element_by_xpath("//*[@id='paginationzt']/li[{}]".format(len(page_list)-1)).find_element_by_tag_name('a').click()
                js = "var q=document.documentElement.scrollTop=0"
                self.browser.execute_script(js)
                time.sleep(1)
            print(com_list)

            for url in com_list:
                try:
                    data = self.get_info(url)
                    print(data)
                    self.sql.insert_data(data,'esta')
                    had_name.append(name)
                except Exception as e:
                    print("获取此企业信息失败：",e)

        try:
            self.browser.switch_to_window(self.browser.window_handles[0])
            self.browser.close()
        except Exception as e:
            print("未关闭此窗口")

        try:
            print("爬取完毕，即将关闭数据库连接")
            self.sql.close_all()
        except Exception as e:
            print("关闭数据库连接失败",e)


    def get_info(self,url):
        # try:
        #     if(len(self.browser.window_handles)>2):
        #         self.browser.close()
        # except Exception as e:
        #     print(e)
        print("窗口个数：",len(self.browser.window_handles))
        data = {}
        self.browser.get(url)
        soup = BeautifulSoup(self.browser.page_source,'lxml')
        tr_list = soup.find('table',attrs={"class":"qxtable"}).find('tbody').find_all("tr")
        #企业注册号
        data["reg_no"] = tr_list[0].find_all('td')[0].find('p').text.strip()
        #企业名称
        data["com_name"] = tr_list[0].find_all('td')[1].find('p').text.strip()
        # #企业类型
        # data["com_type"] = tr_list[1].find_all('td')[0].find('p').text.strip()
        # #负责人
        # data["oper_man"] = tr_list[1].find_all('td')[1].find('p').text.strip()
        # #注册资本
        # data["reg_capi"] = tr_list[2].find_all('td')[0].find('p').text.strip()
        # #成立日期
        # data["start_date"] = tr_list[2].find_all('td')[1].find('p').text.strip()
        # #营业期限自
        # data["date_from"] = tr_list[3].find_all('td')[0].find('p').text.strip()
        # #营业期限至
        # data["date_to"] = tr_list[3].find_all('td')[1].find('p').text.strip()
        # #登记机关
        # data["belong_org"] = tr_list[4].find_all('td')[0].find('p').text.strip()
        # #核准日期
        # data["check_date"] = tr_list[4].find_all('td')[1].find('p').text.strip()
        # #登记状态
        # data["corp_status"] = tr_list[5].find_all('td')[0].find('p').text.strip()
        # #地址
        # data["corp_addr"] = tr_list[6].find_all('td')[0].find('p').text.strip()
        # # 经营范围
        # data["fare_scope"] = tr_list[7].find('td').find('p').text.strip()

        #营业执照信息
        data['yyzz'] = self.browser.find_element_by_xpath("//*[@id='tab_1']/table/tbody").text.strip()

        #获取企业年报信息
        distance = 200
        has_scroll = 0
        while(1):
            try:
                self.browser.execute_script("window.scrollBy(0, {})".format(distance));  # 滚动页面
                has_scroll = has_scroll + distance
                if(has_scroll>5000):
                    print("已到最后")
                    break
                time.sleep(0.2)
            except Exception as e:
                print('滚动出错')
                break
            try:
                qynbxx = self.browser.find_element_by_xpath("//*[@id='qynbxx_yearList']/tbody/tr[1]/td[4]/a")
                qynbxx.click()
            except Exception as e:
                pass
            else:
                break

        time.sleep(3)
        # #企业电话
        # data["com_tel"] = self.browser.find_element_by_xpath("//*[@id='TEL']").text.strip()
        # #企业邮箱
        # data["com_tel"] = self.browser.find_element_by_xpath("//*[@id='E_MAIL']").text.strip()
        # #是否有投资信息或购买其他公司股权
        # data["if_invest"] = self.browser.find_element_by_xpath("//*[@id='IF_INVEST']").text.strip()
        # #是否有对外担保
        # data["if_dwbzdb"] = self.browser.find_element_by_xpath("//*[@id='IF_DWBZDB']").text.strip()
        print(self.browser.window_handles)
        self.browser.switch_to_window(self.browser.window_handles[-1])
        #基本信息
        data['base_info'] = self.browser.find_element_by_id('jibenxinxi').text.strip()

        #对外出资及股东信息
        # info_str = ""
        # pageination = self.browser.find_element_by_class_name("pagination").find_elements_by_tag_name('span')[2:-1]
        # for page in pageination:
        #     page.click()
        #     time.sleep(0.5)
        #     qynb_list = self.browser.find_element_by_xpath("//*[@id='qynbxx_gdczList']").find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')
        #     for qynb in qynb_list:
        #         linewraps = qynb.find_elements_by_tag_name('td')
        #         for wrap in linewraps:
        #             info_str = info_str + '|' + wrap.text.strip()
        try:
            data["gdcz"] = self.browser.find_element_by_xpath("//*[@id='qynbxx_gdczList']/tbody").text
        except Exception as e:
            data["gdcz"] = '无'
        try:
            data['dwcz'] = self.browser.find_element_by_xpath("//*[@id='qynbxx_dwtz_append']").text
            if(data['dwcz']!=''|data['dwcz']!=null):
                add_list = []
                append_com = self.browser.find_element_by_xpath(
                    "//*[@id='qynbxx_dwtz_append']").find_elements_by_tag_name('p')
                for com in append_com:
                    add_list.append(com.text.strip().split('\n')[0])
                print(add_list)
                #self.browser.execute_script("window.open()")
                self.browser.switch_to_window(self.browser.window_handles[-1])
                self.get_all(add_list)
        except Exception as e:
            data['dwcz'] = '无'
            print(e)
        try:
            while(len(self.browser.window_handles)>1):
                self.browser.switch_to_window(self.browser.window_handles[-1])
                self.browser.close()
            self.browser.switch_to_window(self.browser.window_handles[0])
        except Exception as e:
            print(e)
        return data









if __name__ == '__main__':
    crack = Spider()
    # crack.open()
    # crack.crack(u'中国移动')
    # print('验证成功')
    #crack.get_info('http://www.jsgsj.gov.cn:58888/ecipplatform/jiangsu.jsp?org=17BD4BF498C4206C0912FB22EEDAF69A&id=F579E6B04B1EAD18CB8E84DA3C7319C2&seqId=182DCBB20740BE4C2CC1228003FBF934&activeTabId=')
    file = open('F:\python\公司名录\江苏.txt', 'r', encoding='utf-8')
    try:
        lines = file.readlines()
        name_list = []
        for line in lines:
            name_list.append(line.split('\n')[0])
        crack.get_all(name_list)
    except Exception as e:
        print(e)
        file.close()