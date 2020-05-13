#!/usr/bin/env python
# encoding: utf-8
# Author: Guangping ZHANG
# Create Time: 2020/01/04

from src.process.NetBuilder import NetBuilder
import pymongo
from tqdm import tqdm
import numpy as np

NEIGHBOUR_SIZE = 50
myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
mydb = myclient["douyin"]
neighbors = mydb.neighbor
net_builder = NetBuilder()
# vertex_id = []
#
#
# for neighbor in tqdm(neighbors.find()):
#     candidate = [net_builder.getIndex(neighbor['uid'])]
#     ne = sorted(neighbor['neighbor'].items(), key=lambda x: x[1], reverse=True)
#     if len(ne) >= 49:
#         count = 0
#         for t in ne:
#             nei_uid = t[0]
#             if count >= 50:
#                 break
#             nei_id = net_builder.getIndex(nei_uid)
#             candidate.append(nei_id)
#             count += 1
#     else:
#         inter_nodes = []
#         for t in ne:
#             nei_uid = t[0]
#             candidate.append(net_builder.getIndex(nei_uid))
#             inter_nodes.append(nei_uid)
#         gap = 50 - len(candidate)
#         while gap > 0:
#             second_neighbors = {}
#             for nei_uid in inter_nodes:
#                 inter_nodes_neighbor = neighbors.find_one({'uid': nei_uid})
#                 for second_neighbor_uid in inter_nodes_neighbor['neighbor']:
#                     weight = inter_nodes_neighbor['neighbor'][second_neighbor_uid]
#                     second_neighbors[second_neighbor_uid] = weight
#             second_neighbors = sorted(second_neighbors.items(), key=lambda x: x[1], reverse=True)
#             inter_nodes.clear()
#             for t in second_neighbors:
#                 nei_uid = t[0]
#                 candidate.append(net_builder.getIndex(nei_uid))
#                 inter_nodes.append(nei_uid)
#                 gap -= 1
#                 if gap == 0:
#                     break
#     vertex_id.append(candidate)
#
# vertex_id_np = np.zeros([926,50], dtype=int)
# for i in range(926):
#     for j in range(50):
#         vertex_id_np[i][j] = vertex_id[i][j]
# path = '/Users/crescendo/Projects/DouyinDataAnalyse/data/vertex_id.npy'
# np.save(path, vertex_id_np)

# vertex_id = np.load('/Users/crescendo/Projects/DouyinDataAnalyse/data/vertex_id.npy')
#
# adjacency_matrixs = []
# weighted = False
# for vertexs in tqdm(vertex_id):
#     adjacency_matrix = np.zeros([50, 50], dtype=int)
#     for i in range(50):
#         for j in range(i + 1, 50):
#             v1 = vertexs[i]
#             v2 = vertexs[j]
#             if weighted:
#                 adjacency_matrix[i][j] = adjacency_matrix[j][i] = net_builder.adjacency_matrix[v1][v2]
#             else:
#                 if net_builder.adjacency_matrix[v1][v2] != 0:
#                     adjacency_matrix[i][j] = adjacency_matrix[j][i] = 1
#     adjacency_matrixs.append(adjacency_matrix)
#
# adjacency_matrixs = np.array(adjacency_matrixs)
# if weighted:
#     path = '/Users/crescendo/Projects/DouyinDataAnalyse/data/weighted_adjacency_matrix.npy'
# else:
#     path = '/Users/crescendo/Projects/DouyinDataAnalyse/data/adjacency_matrix.npy'
# np.save(path, adjacency_matrixs)


vertex_id = np.load('/Users/crescendo/Projects/DouyinDataAnalyse/data/vertex_id.npy')
labels = np.load('/Users/crescendo/Projects/DouyinDataAnalyse/data/label.npy')
influence_feature = []
for ids in tqdm(vertex_id):
    feature_vector = []
    feature_vector.append([0, 1])
    for i in range(1, 50):
        feature_vector.append([labels[ids[i]], 0])
    influence_feature.append(feature_vector)

influence_feature = np.array(influence_feature, dtype=float)
path = '/Users/crescendo/Projects/DouyinDataAnalyse/data/influence_feature.npy'
np.save(path, influence_feature)
