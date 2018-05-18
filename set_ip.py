from selenium import webdriver
chromeOptions = webdriver.ChromeOptions()

# # 设置代理
# chromeOptions.add_argument("--proxy-server=http://111.170.83.148:8118")
# # 一定要注意，=两边不能有空格，不能是这样--proxy-server = http://202.20.16.82:10152
# browser = webdriver.Chrome(chrome_options = chromeOptions)

# 查看本机ip，查看代理是否起作用
browser.get("http://ip-api.com/line/")
text = browser.page_source
print(text)
browser.get('http://www.jsgsj.gov.cn:58888/province/')
print(browser.page_source)

# # 退出，清除浏览器缓存
# browser.quit()