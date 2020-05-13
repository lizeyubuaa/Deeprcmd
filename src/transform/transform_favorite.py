#!/usr/bin/env python
# encoding: utf-8
# Author: Guangping ZHANG
# Create Time: 2019/12/28

from pymysql import connect
import pymongo
from tqdm import tqdm

myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
mydb = myclient["douyin"]
favorites = mydb.favorite

conn = connect(host='127.0.0.1', port=3306, database='douyin', user='root', password='root', charset='utf8')
cur = conn.cursor()

records = favorites.find()
for record in tqdm(records):
    liker = record['fromuserid']
    author = record['author']['uid']
    sql = 'insert into favorite values (\"{}\", \"{}\")'.format(liker, author)
    cur.execute(sql)
    conn.commit()