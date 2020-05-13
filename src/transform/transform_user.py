#!/usr/bin/env python
# encoding: utf-8
# Author: Guangping ZHANG
# Create Time: 2019/12/28

from pymysql import connect
import pymongo
from tqdm import tqdm

myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
mydb = myclient["douyin"]
users = mydb.users

conn = connect(host='127.0.0.1', port=3306, database='douyin', user='root', password='root', charset='utf8')
cur = conn.cursor()


# 解决sql语句中的引号问题,但是会带来无法接收的效率下降
def checkStr(str):
    pos = str.find('\"')
    while pos != -1:
        str = str[:pos] + "\\" + str[pos:]
        pos = str.find('\"', pos + 2)
    return str


def tf(flag):
    if flag:
        return 'T'
    else:
        return 'F'


pbar = tqdm(total=users.count())
pbar.set_description("Processing Favorite")
for record in tqdm(users.find()):
    user = record['user']
    if 'uid' not in user.keys():
        continue

    uid = user['uid']

    sql = 'select nickname from user where uid = \"{}\"'.format(uid)
    row_count = cur.execute(sql)
    if row_count != 0:
        continue

    nickname = user['nickname']
    signature = user['signature']
    gender = user['gender']
    birthday = user['birthday']
    if birthday == "":
        birthday = '1900-01-01'
    constellation = user['constellation']
    city = user['city']
    custom_verify = user['custom_verify']
    aweme_count = user['aweme_count']
    favoriting_count = user['favoriting_count']
    dongtai_count = user['dongtai_count']
    following_count = user['following_count']
    total_favorited = user['total_favorited']
    follower_count = user['follower_count']
    commerce_user_level = user['commerce_user_level']
    is_star = tf(user['is_star'])
    is_gov_media_vip = tf(user['is_gov_media_vip'])
    is_effect_artist = tf(user['is_effect_artist'])
    live_commerce = tf(user['live_commerce'])
    with_shop_entry = tf(user['with_shop_entry'])
    with_fusion_shop_entry = tf(user['with_fusion_shop_entry'])
    with_commerce_entry = tf(user['with_commerce_entry'])
    with_commerce_enterprise_tab_entry = tf(user['with_commerce_enterprise_tab_entry'])
    with_luban_entry = tf(user['with_luban_entry'])
    with_stick_entry = tf(user['with_stick_entry'])
    sql = 'insert into user(uid, nickname, signature, gender, birthday, constellation, city, custom_verify, ' \
          'aweme_count, favoriting_count, dongtai_count, following_count, total_favorited, follower_count, ' \
          'commerce_user_level, is_star, is_gov_media_vip, is_effect_artist, live_commerce, with_shop_entry, ' \
          'with_fusion_shop_entry, with_commerce_entry, with_commerce_enterprise_tab_entry, with_luban_entry, ' \
          'with_stick_entry) values (\"{}\", \"{}\", \"{}\", {}, \"{}\", {}, \"{}\", \"{}\", {}, {}, {}, {},{}, {}, {}, ' \
          '\"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\") '. \
        format(uid, nickname, signature, gender, birthday, constellation, city, custom_verify, aweme_count,
               favoriting_count,
               dongtai_count, following_count, total_favorited, follower_count, commerce_user_level, is_star,
               is_gov_media_vip,
               is_effect_artist, live_commerce, with_shop_entry, with_fusion_shop_entry, with_commerce_entry,
               with_commerce_enterprise_tab_entry,
               with_luban_entry, with_stick_entry)
    try:
        row_count = cur.execute(sql)
    except Exception as e:
        if e.args[0] == 1064:
            signature = checkStr(signature)
            sql = 'insert into user(uid, nickname, signature, gender, birthday, constellation, city, custom_verify, ' \
                  'aweme_count, favoriting_count, dongtai_count, following_count, total_favorited, follower_count, ' \
                  'commerce_user_level, is_star, is_gov_media_vip, is_effect_artist, live_commerce, with_shop_entry, ' \
                  'with_fusion_shop_entry, with_commerce_entry, with_commerce_enterprise_tab_entry, with_luban_entry, ' \
                  'with_stick_entry) values (\"{}\", \"{}\", \"{}\", {}, \"{}\", {}, \"{}\", \"{}\", {}, {}, {}, {},{}, {}, {}, ' \
                  '\"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\") '. \
                format(uid, nickname, signature, gender, birthday, constellation, city, custom_verify, aweme_count,
                       favoriting_count,
                       dongtai_count, following_count, total_favorited, follower_count, commerce_user_level, is_star,
                       is_gov_media_vip,
                       is_effect_artist, live_commerce, with_shop_entry, with_fusion_shop_entry, with_commerce_entry,
                       with_commerce_enterprise_tab_entry,
                       with_luban_entry, with_stick_entry)
            try:
                row_count = cur.execute(sql)
            except Exception as e:
                if e.args[0] != 1366 and e.args[0] != 1064:
                    print(str(e))
                continue
            # 1366: 非法字符引起的错误，绝大多数与emoji有关
        if e.args[0] != 1366 and e.args[0] != 1064:
            print(str(e))
        continue
    finally:
        conn.commit()
    pbar.update(1)
pbar.close()
