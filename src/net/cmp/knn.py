#!/usr/bin/env python
# encoding: utf-8
# Author: Guangping ZHANG
# Create Time: 2020/01/25

import numpy as np
from tqdm import tqdm
from sklearn.metrics import precision_score, recall_score, f1_score
import sklearn.metrics as sm

NEIGHBOR_SIZE = 9
DATA_PATH = '/Users/crescendo/Projects/DouyinDataAnalyse/data/'

file = 'label.npy'
labels = np.load(DATA_PATH + file)

file = 'weighted_adjacency_matrix.npy'
weighted_adjacency_matrix = np.load(DATA_PATH + file)


def check_add(top_id, top_weight, index, weight):
    for i in range(NEIGHBOR_SIZE):
        if weight >= top_weight[i]:
            top_id.insert(i, index)
            top_weight.insert(i, weight)
            top_id = top_id[:NEIGHBOR_SIZE]
            top_weight = top_weight[:NEIGHBOR_SIZE]
            break
    return top_id, top_weight


def vote(top_id):
    positive = 0
    negative = 0
    for id in top_id:
        if labels[id] == 1:
            positive += 1
        else:
            negative += 1
    if positive * 4 > negative:
        return 1
    else:
        return 0


def get_top(id):
    adj_matrix = weighted_adjacency_matrix[id]
    direct_linked = adj_matrix[0]
    top_id = []
    top_weight = []
    for i in range(NEIGHBOR_SIZE):
        top_id.append(-1)
        top_weight.append(0)
    for i in range(len(direct_linked)):
        top_id, top_weight = check_add(top_id, top_weight, i, direct_linked[i])
    return top_id, top_weight


pred = []
for adj_matrix in tqdm(weighted_adjacency_matrix):
    direct_linked = adj_matrix[0]
    top_id = []
    top_weight = []
    for i in range(NEIGHBOR_SIZE):
        top_id.append(-1)
        top_weight.append(0)
    for i in range(len(direct_linked)):
        top_id, top_weight = check_add(top_id, top_weight, i, direct_linked[i])
    if top_id[-1] == -1:
        stack = []
        for id in top_id:
            stack.append(id)
        while not stack.empty():
            id = stack[0]
            stack.remove(0)
            ti, tw = get_top(id)
            top_id += ti
            stack += ti
            top_weight += tw
            if len(top_id) >= NEIGHBOR_SIZE:
                top_id = top_id[:NEIGHBOR_SIZE]
                top_weight = top_weight[NEIGHBOR_SIZE]
                break
    pred.append(vote(top_id))

precision = precision_score(labels, pred)
print('precision: {}'.format(precision))
recall = recall_score(labels, pred)
print('recall: {}'.format(recall))
f1_score = f1_score(labels, pred)
print('f1 score: {}'.format(f1_score))
from sklearn.metrics import roc_curve, auc
fpr, tpr, th = roc_curve(labels, pred , pos_label=1)
print('AUC: {}'.format(auc(fpr, tpr)))