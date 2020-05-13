#!/usr/bin/env python
# encoding: utf-8
# Author: Guangping ZHANG
# Create Time: 2020/01/04

from pymysql import connect
from tqdm import tqdm
from src.process.Counter import Counter
import numpy as np

counter = Counter()
up_index = 0
vertex_features = []
labels = []

conn = connect(host='127.0.0.1', port=3306, database='douyin', user='root', password='root', charset='utf8')
cur = conn.cursor()

sql = 'select user.uid, user.nickname, user.signature, user.follower_count, user.aweme_count, user.total_favorited, user.hotShop from user, sample ' \
      'where user.uid = sample.uid'
row_count = cur.execute(sql)
ups = cur.fetchall()

for up in tqdm(ups):
    uid = up[0]
    nickname = up[1]
    signature = up[2]
    follower_count = up[3]
    aweme_count = up[4]
    favorited = up[5]
    hotShop = up[6]
    count_vector = counter.count_match(nickname)
    daily = counter.do_daily_detect(nickname)
    count_vector += counter.count_match(signature)
    daily += counter.do_daily_detect(signature)
    sql = 'select description, aweme_id from vedio ' \
          'where author_user_id = \"{}\" '.format(uid)
    row_count = cur.execute(sql)
    if row_count == 0:
        counter.clear_match_counter()
        continue

    # print('{}.'.format(up_index) + nickname + '  vedios in database:{}'.format(row_count))
    up_index += 1
    vedios = cur.fetchall()
    for vedio in vedios:
        description = vedio[0]
        aweme_id = vedio[1]
        count_vector += counter.count_match(description)
        daily += counter.do_daily_detect(description)
        sql = 'select text from comment ' \
              'where aweme_id = \"{}\" ' \
              'order by digg_count desc  '.format(aweme_id)
        row_count = cur.execute(sql)
        # print('>>>  ' + description)
        comments = cur.fetchmany(100)
        for comment in comments:
            text = comment[0]
            count_vector += counter.count_match(text)
            daily += counter.do_daily_detect(text)
            # print('>>>  >>>  ' + text)
    # counter.print_vector(count_vector)
    # print('日常向检测\t{}'.format(daily))
    # counter.save_to_database(uid, daily, count_vector)
    vertex_feature = counter.getVertexFeature(daily, count_vector, follower_count, aweme_count, favorited)
    vertex_features.append(vertex_feature)
    if hotShop == 'T':
        labels.append(1)
    else:
        labels.append(0)
    # sql = 'insert into sample values(\"{}\", \"{}\", {}, {}, {}, \"{}\")' \
    #       ''.format(uid, nickname, follower_count, aweme_count, favorited, hotShop)
    # row_count = cur.execute(sql)
    # conn.commit()
    counter.clear_match_counter()


# sql = 'select uid, nickname, signature, follower_count, aweme_count, total_favorited, hotShop from user ' \
#       'where live_commerce = \"T\" and with_fusion_shop_entry = \"T\" and hotShop = \"F\" ' \
#       'order by rand() limit 800'
# row_count = cur.execute(sql)
# ups = cur.fetchall()
#
# for up in tqdm(ups):
#     uid = up[0]
#     nickname = up[1]
#     signature = up[2]
#     follower_count = up[3]
#     aweme_count = up[4]
#     favorited = up[5]
#     hotShop = up[6]
#     count_vector = counter.count_match(nickname)
#     daily = counter.do_daily_detect(nickname)
#     count_vector += counter.count_match(signature)
#     daily += counter.do_daily_detect(signature)
#     sql = 'select description, aweme_id from vedio ' \
#           'where author_user_id = \"{}\" '.format(uid)
#     row_count = cur.execute(sql)
#     if row_count == 0:
#         counter.clear_match_counter()
#         continue
#
#     # print('{}.'.format(up_index) + nickname + '  vedios in database:{}'.format(row_count))
#     up_index += 1
#     vedios = cur.fetchall()
#     for vedio in vedios:
#         description = vedio[0]
#         aweme_id = vedio[1]
#         count_vector += counter.count_match(description)
#         daily += counter.do_daily_detect(description)
#         sql = 'select text from comment ' \
#               'where aweme_id = \"{}\" ' \
#               'order by digg_count desc  '.format(aweme_id)
#         row_count = cur.execute(sql)
#         # print('>>>  ' + description)
#         comments = cur.fetchmany(100)
#         for comment in comments:
#             text = comment[0]
#             count_vector += counter.count_match(text)
#             daily += counter.do_daily_detect(text)
#             # print('>>>  >>>  ' + text)
#     # counter.print_vector(count_vector)
#     # print('日常向检测\t{}'.format(daily))
#     # counter.save_to_database(uid, daily, count_vector)
#     vertex_feature = counter.getVertexFeature(daily, count_vector, follower_count, aweme_count, favorited)
#     vertex_features.append(vertex_feature)
#     if hotShop == 'T':
#         labels.append(1)
#     else:
#         labels.append(0)
#     sql = 'insert into sample values(\"{}\", \"{}\", {}, {}, {}, \"{}\")' \
#           ''.format(uid, nickname, follower_count, aweme_count, favorited, hotShop)
#     row_count = cur.execute(sql)
#     conn.commit()
#     counter.clear_match_counter()

vertex_features = np.array(vertex_features)
max = vertex_features.max(axis=0)
min = vertex_features.min(axis=0)
gap = max - min
for feature in vertex_features:
    feature = (feature - min) / gap
path = '/Users/crescendo/Projects/DouyinDataAnalyse/data/vertex_feature.npy'
np.save(path, vertex_features, allow_pickle=True)

labels = np.array(labels)
path = '/Users/crescendo/Projects/DouyinDataAnalyse/data/label.npy'
np.save(path, labels, allow_pickle=True)
