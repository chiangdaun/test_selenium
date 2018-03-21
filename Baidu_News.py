#-*- coding:utf-8 -*-
"""
@author:duan
Created on:2018/3/20 21:38
"""
import time
from selenium import webdriver
from setting import *
import pymongo

client = pymongo.MongoClient(MONGO_URI)
db = client[MONGO_DB]

def get_title_url():
    driver = webdriver.Chrome()
    # driver = webdriver.PhantomJS(
    #             executable_path='C:\Program Files (x86)\phantomjs-2.1.1-windows\\bin\phantomjs.exe'
    #             )
    driver.get("http://news.baidu.com/")
    driver.refresh()  # 刷新，有时不能加载出页面

    news_url = [];news_title = []
    title = driver.find_elements_by_xpath('//*[(@class = "pane-news")]//a')

    for news in title:
        news_title.append(news.text)  # 注意此处要加.text获取文本内容
    print(news_title)
    print(len(news_title))

    for i in range(len(news_title)):
        url = title[i].get_attribute('href')  # 此处要写title[i]，从没有解析前的内容中获取URL
        news_url.append(url)

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
    print(data['title'][0])
    for i in range(len(data['title'])):#返回的字典包含所有新闻，拆分为单个，再写入
        if data['title'][i]:
            news_data = {
                'title':data['title'][i],
                'url':data['url'][i]
            }
            save_to_mongo(news_data)
            time.sleep(2)

if __name__ == '__main__':
    main()
