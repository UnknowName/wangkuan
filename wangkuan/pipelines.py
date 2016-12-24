# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import settings
from wangkuan import func


class WangkuanPipeline(object):
    def process_item(self, item, spider):
        return item




class DuolicatePipeline(object):
    def __init__(self):
        self.urls = set()
        self.f = open('urls.log','a+')
    def process_item(self,item,spider):
        if item['url'] in self.urls:
            raise DropItem("Duplicate url found: %s" %(item['url']))
        else:
            pass
            #self.urls.add(item['url'])
        return item



class GzPipeline(object):
    def process_item(self,item,spider):
        company_data = []
        company_data_append = company_data.append
        for k in item:
            company_data_append(item[k])
        status = func.write('company.csv',company_data)
        if status != 200:
            print 'Failed to write csv'
        return item
        
