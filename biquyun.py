#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@Author  :   Jianquan-Wang
@Contact :   1391054830@qq.com
@Desc    :   笔趣阁小说下载，只能单本下载，不支持找到多本小说下载
             win10 + pycharm + selenium + chromedirver
'''

import time
from lxml import etree
from selenium import webdriver


class BiquyuanSpider(object):
    '''笔趣阁的小说搜索下载为txt'''

    def __init__(self):
        self.baseUrl = 'http://www.biquyun.com/'
        # 设置无界面模式
        opt = webdriver.ChromeOptions()
        opt.headless = True
        self.dirver = webdriver.Chrome(options=opt)

    def getBookUrl(self, bookName):
        '''得到全部的url'''
        # 找到搜索框，添加对应内容，点击搜索按钮
        self.dirver.get(self.baseUrl)

        # 页面加载完毕
        searchInput = self.dirver.find_element_by_id('wd')
        searchInput.send_keys(bookName)
        searchBtn = self.dirver.find_element_by_id('sss')
        searchBtn.click()
        time.sleep(1)

        # 网页标签跳转到最新
        windows_1 = self.dirver.current_window_handle
        windows = self.dirver.window_handles
        for current_window in windows:
            if current_window != windows_1:
                self.dirver.switch_to.window(current_window)
        time.sleep(1)

        # 获取页面的内容
        parseHtml = etree.HTML(self.dirver.page_source)

        # 判断是否找到小说
        if self.dirver.page_source.find('<div class="blocktitle">出现错误！</div>') != -1:
            error = parseHtml.xpath('/html/body/div/div/div/div[2]/div[1]/text()[1]')
            print('####搜索错误####')
            for i in error:
                print(i)
        elif self.dirver.page_source.find('<caption>搜索结果</caption>') == -1:
                self.getChapter(parseHtml)
        elif self.dirver.page_source.find('<tr id="nr">') != -1:
            print('找到多本.....')
            print('暂时不支持多本下载，请等待更新....')
        else:
            print("笔趣阁暂时没有这本书！")


    def getChapter(self, parseHtml):
        '''提取页面中所有的url链接'''
        # 获取书的名字
        self.bookName = parseHtml.xpath('//*[@id="info"]/h1/text()')[0]
        # 获取所以章节href
        hrefList = parseHtml.xpath('//div[@id="list"]/dl/dd/a/@href')
        for href in hrefList:
            url = self.baseUrl + href[1:]
            self.parsePage(url)
        print('###全部下载成功###')

    def parsePage(self, url):
        '''处理获取的页面'''
        self.dirver.get(url)
        time.sleep(1)
        # 获取章节名称
        title = self.dirver.find_element_by_xpath('//*[@id="wrapper"]/div[4]/div/div[2]/h1').text
        # 获取文本内容
        content = self.dirver.find_element_by_xpath('//*[@id="content"]').text
        self.writeToTxt(title, content)

    def writeToTxt(self, title, content):
        '''保存在本地为txt'''
        fileName = self.bookName + '.txt'
        with open(fileName, 'a', encoding='utf-8') as f:
            f.write('\r\n')
            f.write(title)
            f.write('\r\n')
            f.write(content)
        print('保存成功>>> '+title)

    def workOn(self):
        '''主程序'''
        name = input("小说名：")
        self.getBookUrl(name)
        self.dirver.quit()


if __name__ == '__main__':
    spider = BiquyuanSpider()
    spider.workOn()
