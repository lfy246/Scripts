# -*- coding:utf-8 -*-
# date 2018/4/26
# author birthpla

import numpy as np
import math
from PIL import Image
from selenium.webdriver.common.action_chains import ActionChains
import time
import random

class easing_slider(object):

    def __init__(self):
        pass

    def ease_out_quad(self,x):
        return 1 - (1 - x) * (1 - x)

    def ease_out_quart(self,x):
        return 1 - pow(1 - x, 4)

    def ease_out_expo(self,x):
        if x == 1:
            return 1
        else:
            return 1 - pow(2, -10 * x)

    def get_tracks(self,distance, seconds):
        tracks = [0]
        offsets = [0]
        for t in np.arange(0.0, seconds, 0.1):
            offset = self.ease_out_quad(t/seconds) * distance
            tracks.append(offset - offsets[-1])
            offsets.append(offset)
        sum = 0
        for i in tracks:
            sum = sum + i
        print(sum)
        print(tracks)
        return offsets, tracks

    def drag_and_drop(self,browser,offset):
        knob = browser.find_element_by_class_name("geetest_slider_button")
        offsets, tracks = self.get_tracks(offset-60, 12)
        ActionChains(browser).click_and_hold(knob).perform()
        for x in tracks:
            ActionChains(browser).move_by_offset(x, 0).perform()
            #time.sleep(random.randint(10,50)/100)
        ActionChains(browser).release(knob).perform()


class count_offset(object):
    def count_x(self,img_1,img_2):
        imgb = Image.open(img_1)
        imgb_array = imgb.load()
        imga = Image.open(img_2)
        imga_array = imga.load()
        # for x in range(325,77,-1):
        #     for y in range(0,105,1):
        #         #print(x," ",y,imgb_array[x,y]," ",imga_array[x,y])
        #         for i in range(4):
        #             if(abs(imgb_array[x,y][i]-imga_array[x,y][i])>50):
        #                 if(abs(imgb_array[x-55,y][i]-imga_array[x-55,y][i])<5):
        #                     print(y)
        #                     return x
        for x in range(324,65,-1):
            for y in range(0,199,1):
                #print(x," ",y,imgb_array[x,y]," ",imga_array[x,y])
                for i in range(4):
                    if(abs(imgb_array[x,y][i]-imga_array[x,y][i])>70):
                        if(abs(imgb_array[x-55,y][i]-imga_array[x-55,y][i])<5):
                            print(y)
                            return x

if __name__=='__main__':
    test_count = count_offset().count_x("after_image.png","fomer_image.png")
    print(test_count)