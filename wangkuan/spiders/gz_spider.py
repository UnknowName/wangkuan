#!/bin/env python
#coding:utf8

from wangkuan import settings
from wangkuan.items import WangkuanItem
from threading import Lock
import scrapy
import requests
import json
import time


PAGE = 1
page_lock = Lock()


class GzSpider(scrapy.Spider):
    name = 'gz'
    base_url = 'http://202.104.65.182:8081/G2/webdrive/web-enterprise!view.do?enterpriseId='
    post_url = ('http://202.104.65.182:8081/G2/gfmweb/web-enterprise!list.do?data'
                '&filter_params_=enterpriseId,rowNum,enterpriseBaseId,enterpriseName,organizationCode'
                '&defined_operations_=&nocheck_operations_=&'
    )
    post_data = {
        'gridSearch':'false',
        'nd':'1482412121211',
        'PAGESIZE':'30',
        'PAGE':'1',
        'sortField':"",
        '_enterpriseName_like':'土',
        'sortDirection':'asc',
        'searchVal':'1',
        'entTypeCodes':""
    }
    s = requests.Session()
    def start_requests(self):
        global PAGE
        resp = self.s.post(
            self.post_url,data=self.post_data,
            headers=settings.DEFAULT_REQUEST_HEADERS
        )
        req_data = json.loads(resp.content)
        total_page = req_data.get('total',None)
        while PAGE < total_page :
            time.sleep(10)
            resp = self.s.post(
                self.post_url,data=self.post_data,
                headers=settings.DEFAULT_REQUEST_HEADERS
            )
            req_data = json.loads(resp.content)
            req_status = req_data.get('success',False)
            if req_status:
                with page_lock:
                    PAGE += 1
                self.post_data['PAGE'] = PAGE
                comp_data = req_data['data']
                for data in comp_data:
                    ent_id = str(data['enterpriseId'])
                    yield scrapy.http.Request(self.base_url+ent_id)
            else:
                print 'Failed go get the %s data' %(page,)


    def parse(self,response):
        item = WangkuanItem()
        company_name = response.xpath('//input[@id="frBaseInfo__M_enterpriseName"]/@value').extract()[0]
        company_reg_addr = response.xpath('//input[@id="frBaseInfo__M_registerAddress"]/@value').extract()[0]
        company_content = response.xpath('//input[@id="frBaseInfo__M_name"]/@value').extract()[0]
        company_phone = response.xpath('//input[@id="frBaseInfo__M_tel"]/@value').extract()[0]
        content_email = response.xpath('//input[@id="frBaseInfo__M_email"]/@value').extract()[0]
        company_org_code = response.xpath('//input[@id="frBaseInfo__M_organizationCode"]/@value').extract()[0]
        org_enddate = response.xpath('//input[@id="licenseValidEndId"]/@value').extract()[0]
        capital = response.xpath('//input[@id="licenseCapital"]/@value').extract()[0]
        item['company_name'] = company_name
        item['company_reg_addr'] = company_reg_addr
        item['company_phone'] = company_phone
        item['company_content'] = company_content
        item['content_email'] = content_email
        item['company_org_code'] = company_org_code + u'\t'
        item['org_enddate'] = org_enddate
        item['capital'] = capital
        print capital
        if item['company_phone'] and item['company_content']:
            return item
