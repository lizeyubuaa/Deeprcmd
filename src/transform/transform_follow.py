#!/usr/bin/env python
# encoding: utf-8
# Author: Guangping ZHANG
# Create Time: 2019/12/28

from pymysql import connect
import pymongo

myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
mydb = myclient["douyin"]
follows = mydb.follow

conn = connect(host='127.0.0.1', port=3306, database='douyin', user='root', password='root', charset='utf8')
cur = conn.cursor()

for record in follows.find():
    for following in record['followings']:
        followed = following['uid']
        follower = record['fromuserid']
        sql = "select * from follow where follower = \"{}\" and followed = \"{}\"".format(follower, followed)
        row_count = cur.execute(sql)
        if row_count != 0:
            continue
        sql = "insert into follow(follower, followed) values (\"{}\", \"{}\")".format(follower, followed)
        row_count = cur.execute(sql)
        conn.commit()
        if row_count == 1:
            print("one follow-pair inserted successfully")
        else:
            print("insert failed")
