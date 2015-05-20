#!/usr/bin/env python
# -*- coding:utf8 -*-
from bs4 import BeautifulSoup
import requests
import sys
import re
import MySQLdb
'''
获取糗事百科
点赞超过5000的段子

'''
req = requests.session()

#点赞数/内容/链接（针对有图片的）存入数据库
def update_mysql(voteNum,listContent,src):
    try:
        conn=MySQLdb.connect(host='localhost',user='root',passwd='3253355',charset='utf8')
        cur=conn.cursor()
        conn.select_db('qsbk')
        values=[voteNum,listContent,src]
        cur.execute('insert into test values(%s,%s,%s)',values)  
        conn.commit()
        cur.close() 
        conn.close()
 
    except MySQLdb.Error,e:
         print "Mysql Error %d: %s" % (e.args[0], e.args[1])

#
def qsbk_info(page):
    url = 'http://www.qiushibaike.com/hot/page/' + str(page)
    r = req.get(url)
    return r.content

def parse_qsbk_info(html):
    # print html
    soup = BeautifulSoup(html)
    listClass = soup.find_all('div','article block untagged mb15') 

    for i in range(0,len(listClass)):
        listImage = listClass[i].find_all('div','thumb')
        voteNum = int(listClass[i].find_all('i','number')[0].get_text())
        listContent = listClass[i].find_all('div','content')[0].get_text().strip()

        if voteNum>5000: 
            if listImage:
                imageSrc = listImage[0].find_all('img')
                src = imageSrc[0].get('src')
            else:                  
                src=''
            update_mysql(voteNum,listContent,src)           

if __name__ == '__main__':
    pageNum = input('输入要抓取的页数：')
    for page in range(1,pageNum+1):
        html = qsbk_info(page)
        parse_qsbk_info(html)
