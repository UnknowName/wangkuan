#!/bin/env python
#coding:utf8

import scrapy
#from wangkuan.items import UrlItem





class BdSpider(scrapy.Spider):
    name = 'bd'
    urls = [
        'https://www.baidu.com/s?wd=%25{keyword}&pn={page}&ct=2097152&tn=baidulocal&ie=utf-8',
    ]

    def start_requests(self):
        page_num = 0
        while page_num <= 11:
            page_num += 10
            req_url = self.urls[0].format(keyword='p2p',page=page_num)
            yield scrapy.http.Request(req_url)

    def parse(self,response):
        urls = [ url for url in response.xpath('//a/@href').extract() 
                 if url.endswith('com/') and 'baidu' not in url
        ]

        for company_url in duplicate_removal(urls):
            yield scrapy.http.Request(company_url,callback=self.parse_company)


    def parse_company(self,response):
        print response.url



