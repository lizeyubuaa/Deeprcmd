#!/usr/bin/env python
# encoding: utf-8
# Author: Guangping ZHANG
# Create Time: 2019/12/28

from pymysql import connect
import pymongo
from tqdm import tqdm

print('start init')
myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
mydb = myclient["douyin"]
favorites = mydb.favorite
neighbor = mydb.neighbor
conn = connect(host='127.0.0.1', port=3306, database='douyin', user='root', password='root', charset='utf8')
cur = conn.cursor()
print('finished.')


print('\nstart loading sample uid')
sql = 'select uid from sample'
row_count = cur.execute(sql)
row_all = cur.fetchall()
samples = {}
samples_uid = []
for row in tqdm(row_all):
    samples[row[0]] = {}
    samples_uid.append(row[0])

print('\nstart loading favorite data')
sql = 'select * from favorite order by liker'
row_count = cur.execute(sql)
row_all = cur.fetchall()
print('finished.')


print('\nstart matching')
liker = ''
related_authors = []
for row in tqdm(row_all):
    if row[0] != liker:
        if len(related_authors) > 1:
            for author in related_authors:
                # 添加记录
                for au in related_authors:
                    if au == author:
                        continue
                    if au in samples[author].keys():
                        samples[author][au] += 1
                    else:
                        samples[author][au] = 1
        related_authors.clear()
        liker = row[0]
    liked = row[1]
    if liked in samples_uid:
        related_authors.append(liked)

print('\nstart writing database')
dics = []
for sample in tqdm(samples):
    dic = {'uid': sample, 'neighbor': samples[sample]}
    dics.append(dic)
neighbor.insert_many(dics)

