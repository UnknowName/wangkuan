# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WangkuanItem(scrapy.Item):
    "最终要抓取的数据"
    company_name = scrapy.Field() #公司名称
    company_reg_addr = scrapy.Field() #公司注册所在地址
    company_phone = scrapy.Field() #公司联系电话
    company_content = scrapy.Field() #公司联系人
    content_email = scrapy.Field() #联系人Email
    company_org_code = scrapy.Field() #组织机构代码编号
    org_enddate = scrapy.Field() #组织机构代码到期日期
    capital = scrapy.Field()#注册资本


class UrlItem(scrapy.Item):
    "用以去重，临时存储的"
    url = scrapy.Field()
