from selenium import webdriver

class maigoo(object):
    def __init__(self):
        self.driver = webdriver.Chrome('F:\\python\chromedriver.exe')
        self.file = ""

    def scroll(self,url,file):
        self.driver.get(url)
        block = self.driver.find_element_by_class_name("load_block").find_elements_by_tag_name('dl')
        self.file = file
        for dl in block:
            data = []
            dds = dl.find_elements_by_tag_name('dd')
            for dd in dds:
                text = dd.find_element_by_class_name('resultinfo').find_elements_by_tag_name('div')[1].find_element_by_tag_name('div').text
                data.append(text.split('（')[0])
        try:
            while(1):
                try:
                    self.driver.find_element_by_xpath("//*[@id='container']/div[1]/div[3]/a").click()
                    self.driver.execute_script("window.scrollBy(0, 800)")
                except Exception as e:
                    break
                else:
                    data = []
                    dl = self.driver.find_element_by_class_name("load_block").find_elements_by_tag_name('dl')[-1]
                    dds = dl.find_elements_by_tag_name('dd')
                    for dd in dds:
                        text = dd.find_element_by_class_name('resultinfo').find_elements_by_tag_name('div')[1].find_element_by_tag_name('div').text
                        data.append(text.split('（')[0]+'\n')
                    self.save(data)
        except Exception as e:
            self.file.close()
            print(e)

    def save(self,data):
        for d in data:
            self.file.write(d)
        print(data,"写入成功")

    def get_com(self):
        file = open('maigoo.txt','r')
        data = file.readlines()
        print(data)
        return data


if __name__=='__main__':
    spider = maigoo()
    provice = open("F:\python\公司名录\provinces.txt",'r',encoding='utf-8')
    lines = provice.readlines()
    for line in lines:
        file = open("F:\python\公司名录\{}.txt".format(line.split(' ')[0]),'a',encoding='utf-8')
        spider.scroll("http://www.maigoo.com/brand/search/?areaid={}".format(line.split(' ')[1]),file)
    provice.close()

