#!/usr/bin/env python
# encoding: utf-8
# Author: Guangping ZHANG
# Create Time: 2019/12/28

from pymysql import connect
import pymongo

myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
mydb = myclient["douyin"]
hotShops = mydb.hotShop

conn = connect(host='127.0.0.1', port=3306, database='douyin', user='root', password='root', charset='utf8')
cur = conn.cursor()


authors = []
goods = []
for record in hotShops.find():
    data = record['data']
    special = data['special']
    rank_list = data['rank_list']
    for item in rank_list:
        author_id = item['author']['id']
        author_name = item['author']['name']
        good = item['goods']['title']
        sql = 'select uid from user ' \
              'where uid = \"{}\" '.format(author_id)
        row_count = cur.execute(sql)
        if row_count == 0:
            continue
        else:
            sql = 'update user set hotShop = \"T\" ' \
                  'where uid = \"{}\" '.format(author_id)
            row_count = cur.execute(sql)
            conn.commit()
        # if row_count == 1:
        #     print("one hotShop inserted successfully")
        # else:
        #     print("insert failed")