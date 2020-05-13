#!/usr/bin/env python
# encoding: utf-8
# Author: Guangping ZHANG
# Create Time: 2019/12/28

from pymysql import connect
import pymongo
from tqdm import tqdm

myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
mydb = myclient["douyin"]
comments = mydb.comment

conn = connect(host='127.0.0.1', port=3306, database='douyin', user='root', password='root', charset='utf8')
cur = conn.cursor()


def loadReply(fromid, reply):
    cid = reply['cid']
    text = reply['text']
    if text.startswith('@'):
        return
    aweme_id = reply['aweme_id']
    digg_count = reply['digg_count']
    uid = reply['user']['uid']
    is_author_digged = 'F'
    if reply['is_author_digged']:
        is_author_digged = 'T'
    reply_comment_total = '0'
    if reply['reply_comment'] != None:
        reply_comment_total = len(reply['reply_comment'])
        for rereply in reply['reply_comment']:
            loadReply(cid, rereply)
    to_cid = fromid

    sql = "select cid from comment where cid = \"{}\"".format(cid)
    row_count = cur.execute(sql)
    if row_count != 0:
        return
    sql = "insert into comment(cid, text, aweme_id, digg_count, uid, is_author_digged, reply_comment_total, to_cid) values (\"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\")" \
        .format(cid, text, aweme_id, digg_count, uid, is_author_digged, reply_comment_total, to_cid)
    try:
        row_count = cur.execute(sql)
    except Exception as e:
        pass
        # print(str(e))
    conn.commit()
    # if row_count != 1:
    #     print("insert failed")


for record in tqdm(comments.find()):
    if record['comments'] == None:
        continue
    for comment in record['comments']:
        cid = comment['cid']
        text = comment['text']
        if text.startswith('@'):
            continue
        aweme_id = comment['aweme_id']
        digg_count = comment['digg_count']
        uid = comment['user']['uid']
        is_author_digged = 'F'
        if comment['is_author_digged']:
            is_author_digged = 'T'
        reply_comment_total = '0'
        if comment['reply_comment'] != None:
            reply_comment_total = len(comment['reply_comment'])
            for rereply in comment['reply_comment']:
                loadReply(cid, rereply)
        to_cid = "0"

        sql = "select cid from comment where cid = \"{}\"".format(cid)
        row_count = cur.execute(sql)
        if row_count != 0:
            continue
        sql = "insert into comment(cid, text, aweme_id, digg_count, uid, is_author_digged, reply_comment_total, to_cid) values (\"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\")" \
            .format(cid, text, aweme_id, digg_count, uid, is_author_digged, reply_comment_total, to_cid)
        try:
            row_count = cur.execute(sql)
        except Exception as e:
            pass
            # print(str(e))
        conn.commit()
        # if row_count != 1:
        #     print("insert failed")
