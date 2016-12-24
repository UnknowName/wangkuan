#!/bin/env python
#coding:UTF8

import csv



def encode(s):
    "将unicode解码为utf8"
    if isinstance(s, unicode):
        return s.encode('utf8')
    else:
        return s

def write(file_name,iter_obj,heads=[]):
    "定义写入CSV文件，iter_obj是List或者db-cursor,heads是标题列"
    with open(file_name,'ab') as csv_file:
        csv_wr = csv.writer(csv_file,
            delimiter=',',  #分隔符,默认为","。如果指定错了，会将列表中的字符串连接在一起了
            quotechar='"',  #特殊符号前加符号
            quoting=csv.QUOTE_MINIMAL
        )
        heads = map(encode,heads)
        if heads:
            csv_wr.writerow(heads)#写入表头
        if isinstance(iter_obj, list):
            iter_obj = map(encode,iter_obj)
            #写入CSV文件内容，一个列表。eg['name1','age1'],['name2','age2']
            csv_wr.writerow(iter_obj) 
        else:
            #下面是针对数据库cursor对象的情况
            for lst in iter_obj:
                lst = map(encode,lst)
                csv_wr.writerow(lst)
        return 200
    
