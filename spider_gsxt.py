# -*-coding:utf-8 -*-

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from PIL import Image
import pytesseract
from selenium.webdriver.support.ui import WebDriverWait
from urllib.request import urlretrieve
import time
import img_ope


class spider_gsxt(object):
    def __init__(self, com_name, url):  # 公司名称
        self.com_name = com_name
        self.url= url
        self.driver = webdriver.Chrome(executable_path='F:\python\chromedriver.exe')
        self.wait = WebDriverWait(self.driver,100)
        self.index = 0

    def open_geetest(self):
        try:
            time.sleep(2)
            self.driver.get(self.url)
            keyword = self.wait.until(EC.presence_of_element_located((By.ID, 'keyword')))
            keyword.click()
            keyword.send_keys(self.com_name)
            time.sleep(2)
            button = self.driver.find_element_by_id('btn_query')
            button.click()
        except Exception as e:
            print("open failed! ",e)
            self.driver.quit()
        else:
            print("open sucessfully!")




    def get_images(self):
        try:
            time.sleep(2)
            bg_image = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_item_img')))
            image_url = bg_image.get_attribute("src")
            print(image_url)
            urlretrieve(image_url, filename='F:\images\gee_img.jpg')
        except Exception as e:
            self.driver.quit()
            print(e)
        else:
            self.index = self.index + 1





    def break_geetest(self):
        self.open_geetest()
        self.get_images()

    def click_position(self,tips,image):
        positions = []
        return positions

    def get_tips(self,tips_image):
        tips = pytesseract.image_to_string(Image.open(tips_image), lang='chi_sim') #ocr简单识别
        return list(tips)          #把关键字符串转换成list

if __name__ == '__main__':
    test = spider_gsxt("中国移动","http://js.gsxt.gov.cn/index.html")
    test.break_geetest()
