#-*- coding:utf-8 -*-
"""
@author:duan
Created on:2018/3/21 15:15
"""
import time
from selenium import webdriver
from setting import *
import pymongo

client = pymongo.MongoClient(MONGO_URI)
db = client[MONGO_DB]

def get_title_url():
    #driver = webdriver.Chrome()
    driver = webdriver.PhantomJS(
                executable_path='C:\Program Files (x86)\phantomjs-2.1.1-windows\\bin\phantomjs.exe'
                )
    driver.get("http://news.baidu.com/")
    driver.refresh()  # 刷新，有时不能加载出页面

    news_url = [];news_title = []

    #抓取'热点要闻'
    pane_news_title = driver.find_elements_by_xpath('//*[(@id = "pane-news")]//a')
    for news in pane_news_title:
        news_title.append(news.text)  # 注意此处要加.text获取文本内容
    for i in range(len(pane_news_title)):
        url = pane_news_title[i].get_attribute('href')  # 此处要写title[i]，从没有解析前的内容中获取URL
        news_url.append(url)
    time.sleep(2)

    #抓取'本地新闻'
    localnews_focus_title = driver.find_elements_by_xpath('//*[(@id = "localnews-focus")]//a')
    for news in localnews_focus_title:
        news_title.append(news.text)  # 注意此处要加.text获取文本内容
    for i in range(len(localnews_focus_title)):
        url = localnews_focus_title[i].get_attribute('href')  # 此处要写title[i]，从没有解析前的内容中获取URL
        news_url.append(url)
    time.sleep(2)

    #抓取'新闻资讯'
    localnews_zixun_title = driver.find_elements_by_xpath('//*[(@id = "localnews-zixun")]//a')
    for news in localnews_zixun_title:
        news_title.append(news.text)  # 注意此处要加.text获取文本内容
    for i in range(len(localnews_zixun_title)):
        url = localnews_zixun_title[i].get_attribute('href')  # 此处要写title[i]，从没有解析前的内容中获取URL
        news_url.append(url)
    time.sleep(2)

    guoneinews_left_title = driver.find_elements_by_xpath('//div[(@alog-group = "log-civil-left")]//a')
    print(guoneinews_left_title)
    for news in guoneinews_left_title:
        news_title.append(news.text)  # 注意此处要加.text获取文本内容
    for i in range(len(guoneinews_left_title)):
        url = guoneinews_left_title[i].get_attribute('href')  # 此处要写title[i]，从没有解析前的内容中获取URL
        news_url.append(url)
    time.sleep(2)

    '''
    待解决问题：
            只抓取了热点新闻和本地新闻，后面的国际国内等新闻未能抓取，
            抓取到的均是利用id="XXX"进行的，其后的新闻没有id属性，
            (虽然有id="guonei"，但是并不能抓到内容)，然后当利用
            class属性抓取时，也并不能抓得到内容。
    '''

    # left_title = driver.find_elements_by_class_name("l-left-col")
    # print(left_title)
    #
    # for news in left_title:
    #     if news.text :
    #         news_title.append(news.text)  # 注意此处要加.text获取文本内容
    # # for i in range(len(left_title)):
    # #     url = left_title[i].get_attribute('href')  # 此处要写title[i]，从没有解析前的内容中获取URL
    # #     news_url.append(url)
    # time.sleep(2)

    print(news_title)
    print(len(news_title))
    print(news_url)
    print(len(news_url))
    driver.quit()
    return {
        'title':news_title,
        'url':news_url
    }

def save_to_mongo(data):
    crawl_time = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    #这种时间格式('%Y-%m-%d %H:%M:%S')，不能作为文件名，但可以作为数据库表名
    print(crawl_time)
    if db[crawl_time].update({'title':data['title']},{'$set':data},True):
        print('Saved to Mongo',data['title'])
    else:
        print('Saved to Mongo Failed',data['title'])

def main():
    data = get_title_url()
    print(len(data['title']))
    if len(data['title']) != 0:#判断是否抓取到内容，如果因为数据没有加载出来，则执行else再次打开
        for i in range(len(data['title'])):#返回的字典包含所有新闻，拆分为单个，再写入
            if data['title'][i]:
                news_data = {
                    'title':data['title'][i],
                    'url':data['url'][i]
                }
                save_to_mongo(news_data)
    else:
        get_title_url()


if __name__ == '__main__':
    main()