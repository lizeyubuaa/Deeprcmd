#!/usr/bin/env python
# encoding: utf-8
# Author: Guangping ZHANG
# Create Time: 2019/12/28

from pymysql import connect
import pymongo


class database:
    def __init__(self):
        self.myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
        self.mydb = self.myclient["douyin"]

        self.conn = connect(host='127.0.0.1', port=3306, database='douyin', user='root', password='root',
                            charset='utf8')
        self.cur = self.conn.cursor()

    def getFollowers(self, id):
        sql = "select follower from follow where followed = \"{}\"".format(id)
        row_count = self.cur.execute(sql)
        row_all = self.cur.fetchall()
        followers = []
        for row in row_all:
            followers.append(row[0])
        return followers

    def getFolloweds(self, id):
        sql = "select followed from follow where follower = \"{}\"".format(id)
        row_count = self.cur.execute(sql)
        row_all = self.cur.fetchall()
        followeds = []
        for row in row_all:
            followeds.append(row[0])
        return followeds

    def getComments(self, id):
        sql = "select text from comment where aweme_id = \"{}\"".format(id)
        row_count = self.cur.execute(sql)
        row_all = self.cur.fetchall()
        comments = []
        for row in row_all:
            comments.append(row[0])
        return comments

    # 84990209480 陈赫
    def getAweme(self, id):
        sql = "select aweme_id, description from vedio where author_user_id = \"{}\"".format(id)
        row_count = self.cur.execute(sql)
        row_all = self.cur.fetchall()
        decriptions = []
        for row in row_all:
            aweme = {}
            aweme['aweme_id'] = row[0]
            aweme['description'] = row[1]
            decriptions.append(aweme)
        return decriptions

    def getAwemeTags(self, id):
        sql = "select aweme_id, text_extra from vedio where author_user_id = \"{}\"".format(id)
        row_count = self.cur.execute(sql)
        row_all = self.cur.fetchall()
        decriptions = []
        for row in row_all:
            if row[1] == "":
                continue
            aweme = {}
            aweme['aweme_id'] = row[0]
            aweme['text_extra'] = row[1]
            decriptions.append(aweme)
        return decriptions
