#!/usr/bin/env python
# encoding: utf-8
# Author: Guangping ZHANG
# Create Time: 2019/12/28

import numpy as np

path1 = '/Users/crescendo/Projects/FromGithub/DeepInf/data/weibo/weibo/influence_feature.npy'
path2 = '/Users/crescendo/Projects/DouyinDataAnalyse/data/influence_feature.npy'

preview1 = np.load(path1)
preview2 = np.load(path2)


pass

# positive = preview[:201]
# negative = preview[201:]
#
# print('positive: ')
# print(positive.mean(axis=0))
#
# print('negative: ')
# print(negative.mean(axis=0))