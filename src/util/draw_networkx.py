#!/usr/bin/env python
# encoding: utf-8
# Author: Guangping ZHANG
# Create Time: 2020/01/04

from src.process.NetBuilder import NetBuilder
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

net_builder = NetBuilder()
G = nx.Graph()
for i in range(925):
    G.add_node(i+1)
G.add_weighted_edges_from(net_builder.edges)
path = '/Users/crescendo/Projects/DouyinDataAnalyse/data/label.npy'
labels = np.load(path)
colors = []
for label in labels:
    if label == 1:
        colors.append('r')
    else:
        colors.append('b')
nx.draw(G,label=labels, node_color=colors, edge_color='gray', with_labels=True, font_size=4, node_size=10, width=0.01)
plt.show()
