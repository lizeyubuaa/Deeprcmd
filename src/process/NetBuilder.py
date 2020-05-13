#!/usr/bin/env python
# encoding: utf-8
# Author: Guangping ZHANG
# Create Time: 2020/01/04

from pymysql import connect
import pymongo
from tqdm import tqdm
import numpy as np

class NetBuilder:
    conn = connect(host='127.0.0.1', port=3306, database='douyin', user='root', password='root', charset='utf8')
    cur = conn.cursor()
    myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
    mydb = myclient["douyin"]
    neighbor = mydb.neighbor
    adjacency_matrix = np.eye(926, dtype=int)
    edges = []
    islands = []
    uid_index = {}

    def loadUidIndexDic(self):
        sql = 'SELECT @rowNum:=@rowNum + 1 AS ‘index’,a.uid FROM sample a,(SELECT @rowNum:=0) b '
        row_count = self.cur.execute(sql)
        row_all = self.cur.fetchall()
        for row in row_all:
            self.uid_index[row[1]] = int(row[0] - 1)

    def getIndex(self, uid):
        return self.uid_index[uid]

    def __init__(self):
        self.loadUidIndexDic()
        neighbors = self.neighbor.find()
        for ne in neighbors:
            id1 = self.getIndex(ne['uid'])
            if len(ne['neighbor']) == 0:
                self.islands.append(ne['uid'])
                continue
            for neib in ne['neighbor']:
                id2 = self.getIndex(neib)
                self.adjacency_matrix[id1][id2] = int(ne['neighbor'][neib])
                if id2 <= id1:
                    continue
                weight = ne['neighbor'][neib]
                self.edges.append((id1, id2, weight))
