#!/usr/bin/env python
# encoding: utf-8
# Author: Guangping ZHANG
# Create Time: 2019/12/28

from pymysql import connect
import pymongo

myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
mydb = myclient["douyin"]
hotSearch = mydb.db_hotSearch

conn = connect(host='127.0.0.1', port=3306, database='douyin', user='root', password='root', charset='utf8')
cur = conn.cursor()


authors = []
goods = []
for record in hotSearch.find():
    pass