#!/bin/env python
#coding:utf8


import scrapy
from scrapy.http import Request


class BaiduSpider(scrapy.Spider):
    name = 'baidu'

    #def __init__(self):
    #    self.url = 'https://www.baidu.com'

    start_urls = [
        'https://www.baidu.com/s?wd=%25{keyword}&pn={page}&ct=2097152&tn=baidulocal&ie=utf-8'
    ]
    
    def parse(self,response):
        "提取通过关键词百度展现的页面的"
        urls = [ url.split('/')[0] for url in response.xpath('//a/text()').extract() if url.startswith('www')]
        next_page_url = [ page for page in response.xpath('//div[@id="page"]/a/@href').extract() if 'page' in page ][0]
        urls.append(next_page_url)
        with open('urls.txt','a+') as f:
            for url in urls:
                f.write(url.encode('utf8')+'\n')
                #f.write(next_page_url.encode('utf8')+'\n')
        for url in urls:
            if 'page' in url:
                with open('new.log','a+') as f:
                    f.write(url.encode('utf8'+'\n')) 
                yield Request(u'https://www.baidu.com'+url,callback=self.parse)
                continue
            #yield Request('http://'+url,callback=self.parse_item)
             
             
    def parse_item(self,response):
        "提取从百度抓取到的相关公司的函数"
        pass
#c = BaiduSpider()
#c.parse('ss')


