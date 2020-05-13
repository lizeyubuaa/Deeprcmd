#!/usr/bin/env python
# encoding: utf-8
# Author: Guangping ZHANG
# Create Time: 2020/01/07

import numpy as np
from tqdm import tqdm
from src.process.NetBuilder import NetBuilder


net_builder = NetBuilder()
adjlist_prepath = '/Users/crescendo/Projects/DouyinDataAnalyse/data/adjlist/full_net.adjlist'
adjlist = open(adjlist_prepath, 'w')

lines = []
for i in tqdm(range(926)):
    line = '{}'.format(i+1)
    for j in range(926):
        if i == j:
            continue
        if net_builder.adjacency_matrix[i][j] == 1:
            line += ' {}'.format(j+1)
    line += '\n'
    lines.append(line)

adjlist.writelines(lines)
adjlist.close()


