#!/usr/bin/env python
# encoding: utf-8
# Author: Guangping ZHANG
# Create Time: 2020/01/04

from src.process.NetBuilder import NetBuilder
from pymysql import connect

conn = connect(host='127.0.0.1', port=3306, database='douyin', user='root', password='root', charset='utf8')
cur = conn.cursor()
net_builder = NetBuilder()
islands = net_builder.islands

for island in islands:
    sql = 'delete from sample where uid = \"{}\"'.format(island)
    cur.execute(sql)
    conn.commit()
