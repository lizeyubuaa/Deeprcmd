#!/usr/bin/env python
# encoding: utf-8
# Author: Guangping ZHANG
# Create Time: 2020/01/04

import numpy as np
from pymysql import connect

'''
@ description:
    本类用于加载关键词并进行匹配操作
    实现从up的视频描述和评论区的文本信息中提取出up在商品类别上的倾向性

@ categories: 
    服装
    奢侈品
    美妆
    母婴
    家电家具家纺
    数码
    汽车
    水果食品饮料
    医疗
    财经法律
    动漫 
    
    日常向检测

@ 其他备选参考变量：
    用户衡量up的专业性/专一性：
        匹配命中率
        cate向量方差
'''


class Counter:
    conn = connect(host='127.0.0.1', port=3306, database='douyin', user='root', password='root', charset='utf8')
    cur = conn.cursor()
    cates = ['服装', '奢侈品', '美妆', '母婴', '家电家具家纺', '数码', '汽车', '水果食品饮料', '医疗', '财经法律', '动漫']
    keywords = []
    daily_detect = []
    match_counter = 0

    def __init__(self):
        for cate in self.cates:
            path = '/Users/crescendo/Projects/DouyinDataAnalyse/resource/wordbase/' + cate + '.text'
            file = open(path, 'r')
            words = file.readlines()
            cate_keywords = []
            for word in words:
                cate_keywords.append(word[:-1])
            self.keywords.append(cate_keywords)

        path = '/Users/crescendo/Projects/DouyinDataAnalyse/resource/wordbase/' + '日常向检测' + '.text'
        file = open(path, 'r')
        words = file.readlines()
        for word in words:
            self.daily_detect.append(word[:-1])

    def do_daily_detect(self, str):
        count = 0
        for keyword in self.daily_detect:
            if str.find(keyword) != -1:
                count += 1
        return count

    def count_match(self, str):
        count_result = []
        for cate_keywords in self.keywords:
            count = 0
            for keyword in cate_keywords:
                if str.find(keyword) != -1:
                    count += 1
            count_result.append(count)
        count_result = np.array(count_result)
        self.match_counter += 1
        return count_result

    def print_vector(self, vector):
        sum = np.sum(vector)
        size = len(self.cates)
        for i in range(size):
            print(self.cates[i] + '\t{}\t占比\t{}%'.format(vector[i], format(vector[i] / sum * 100, '.2f')))
        print('匹配次数\t{}'.format(self.match_counter))
        print('命中次数\t{}'.format(sum))
        print('命中率\t{}%'.format(format(sum / self.match_counter * 100, '.2f')))
        print('向量方差\t{}'.format(format(np.var(vector / sum)), '.2f'))

    def clear_match_counter(self):
        self.match_counter = 0

    def save_to_database(self, uid, daily, vector):
        sql = 'insert into user_embedding values (\"{}\", {}, {},  {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}) ' \
              ''.format(uid, daily, self.match_counter, vector[0], vector[1], vector[2], vector[3], vector[4],
                        vector[5], vector[6], vector[7],
                        vector[8], vector[9], vector[10], vector[11], vector[12], vector[13], vector[14])
        row_count = self.cur.execute(sql)
        self.conn.commit()

    def getVertexFeature(self, daily, vector, follower, aweme, favorated):
        vertex_feature = []
        sum = np.sum(vector)
        if sum != 0:
            vector = vector / sum
        for element in vector:
            vertex_feature.append(element)  # 各品类的比重
        vertex_feature.append(sum / self.match_counter)  # 匹配命中率
        vertex_feature.append(np.var(vector))  # 向量方差
        vertex_feature.append(daily / self.match_counter)  # 日常向内容比例
        vertex_feature.append(follower)  # 粉丝数
        vertex_feature.append(aweme)  # 视频数
        vertex_feature.append(favorated)  # 获赞数目
        return vertex_feature
