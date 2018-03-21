from selenium import webdriver
from lxml import etree
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
driver.get("http://news.baidu.com/")
#time.sleep(3)

#driver.set_window_size(800,800)

# #访问百度首页
# first_url= 'http://www.baidu.com'
# print("now access %s" %(first_url))
# driver.get(first_url)

# #访问新闻页面
# second_url='http://news.baidu.com'
# print("now access %s" %(second_url))
# driver.get(second_url)
#
# #返回（后退）到百度首页
# print("back to  %s "%(first_url))
# driver.back()
#
# #前进到新闻页
# print("forward to  %s"%(second_url))
# driver.forward()

# driver.find_element_by_id("kw").clear()
# driver.find_element_by_id("kw").send_keys("西南科技大学")
# driver.find_element_by_class_name("bg").click()

# search_text = driver.find_element_by_id('kw')
# search_text.send_keys('selenium')
# search_text.submit()

# # 获得输入框的尺寸
# size = driver.find_element_by_id('kw').size
# print(size)
#
# # 返回百度页面底部备案信息
# text = driver.find_element_by_id("cp").text
# print(text)
#
# 返回元素的属性值， 可以是 id、 name、 type 或其他任意属性
# attribute = driver.find_element_by_id("kw").get_attribute('type')
# print(attribute)
#
# # 返回元素的结果是否可见， 返回结果为 True 或 False
# result = driver.find_element_by_id("kw").is_displayed()
# print(result)

# element = WebDriverWait(driver, 5, 0.5).until(
#                       EC.presence_of_element_located((By.ID, "kw"))
#                       )
# element.send_keys('selenium')

# driver.find_element_by_id("kw").send_keys("西南科技大学")
# driver.find_element_by_id("su").click()
# time.sleep(3)
# # 定位一组元素
# texts = driver.find_elements_by_xpath('//div/h3/a')
# # 循环遍历出每一条搜索结果的标题
# title = []
# for t in texts:
#     print(t.text)
#     title.append(t.text)
# # print(title)
# print(len(title))
# urls = []
# for i in range(len(title)):
#     url = texts[i].get_attribute('href')#get_attribute()抓取属性值，每次只抓取到一个，要通过循环来全部抓取
#     urls.append(url)
#     print(url)
# print(len(urls))

#news1实现打开百度首页，点击新闻，news2不行，是list对象没有click()属性
# news1 = driver.find_element_by_xpath(
#     '//*[contains(concat( " ", @class, " " ), concat( " ", "mnav", " " )) and (((count(preceding-sibling::*) + 1) = 1) and parent::*)]').click()
#news2 = driver.find_elements_by_css_selector('.mnav:nth-child(1)').click()

news_url = [];news_title = []
title = driver.find_elements_by_xpath('//*[(@id = "pane-news")]//a')

for news in title:
    news_title.append(news.text)#注意此处要加.text获取文本内容
print(news_title)
print(len(news_title))

for i in range(len(news_title)):
    url = title[i].get_attribute('href')#此处要写title[i]，从没有解析前的内容中获取URL
    news_url.append(url)

print(news_url)
print(len(news_url))

crawl_time = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
#这种时间格式('%Y-%m-%d %H:%M:%S')，不能作为文件名
print(crawl_time)

#把抓取到的新闻标题和链接写入文档
filename = 'E:\crawl_data\Baidu_News\\'+ crawl_time +'.txt'
with open(filename,'a') as f:
    if len(news_url) == len(news_title):
        for i in range(len(news_title)):
            f.write(news_title[i] + ': ' + news_url[i])
            f.writelines('\n\n')

# driver.refresh()
# time.sleep(3)
driver.quit()