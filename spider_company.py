# -*- coding:utf-8 -*-
# date 2018/4/26
# author birthpla
from selenium import webdriver
import drop_slider
import time
from selenium.webdriver.common.action_chains import ActionChains

class spider_company(object):
    def __init__(self,com_name,url):      #公司名称
        self.com_name = com_name
        self.url = url
        self.driver = webdriver.Firefox(executable_path='F:\python\geckodriver.exe')

    def get_info(self):
        self.driver.get(self.url)
        for i in range(10):  # 尝试验证十次
            time.sleep(1)
            former = self.driver.current_url
            if (self.url != former):
                break
            if (i == 9):
                print("验证失败")
                return
            print("正在进行第 ", i + 1, " 次验证")
            self.driver.get(self.url)
            input = self.driver.find_element_by_xpath("//*[@id='name']")
            while (1):
                try:
                    input.click()
                except Exception as e:
                    time.sleep(1)
                    print(e)
                else:
                    break
            input.send_keys(self.com_name)
            button = self.driver.find_element_by_xpath("//*[@id='popup-submit']")
            while (1):
                try:
                    button.click()
                except Exception as e:
                    time.sleep(1)
                    print(e)
                else:
                    break
            time.sleep(3)
            fomer_image = self.driver.find_element_by_class_name("gt_box")
            fomer_image.screenshot('fomer_image.png')
            slider_click = self.driver.find_element_by_xpath("/html/body/div[4]/div[2]/div[2]/div[2]/div[2]")
            slider_click.click()
            self.driver.implicitly_wait(10)
            after_image = self.driver.find_element_by_class_name("gt_box")
            after_image.screenshot('after_image.png')
            offset = drop_slider.count_offset().count_x('fomer_image.png', 'after_image.png')
            print("计算出的偏移量是： ", offset)
            time.sleep(1)
            #drop_slider.easing_slider().drag_and_drop(self.driver, offset)
            knob = self.driver.find_element_by_xpath("//div[@class='gt_slider_knob gt_show']")
            ActionChains(self.driver).drag_and_drop_by_offset(knob,offset,0).perform()




if __name__ =='__main__':
    spider = spider_company("星网","http://js.gsxt.gov.cn/index.html")
    spider.get_info()



