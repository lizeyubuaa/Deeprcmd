#!/usr/bin/env python
# encoding: utf-8
# Author: Guangping ZHANG
# Create Time: 2020/01/25

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
import sklearn.metrics as sm
from sklearn.metrics import precision_score, recall_score, f1_score

path = '/Users/crescendo/Projects/DouyinDataAnalyse/data/vertex_feature.npy'
vertex_features = np.load(path)

path = '/Users/crescendo/Projects/DouyinDataAnalyse/data/deepwalk.emb_64'
emb_file = open(path)
size = emb_file.readline()[:-1].split()
length = int(size[0])
dim = int(size[1])
emb = np.zeros([length, dim])
for i in range(length):
    data = emb_file.readline()[:-1].split()
    index = int(data[0]) - 1
    for i in range(dim):
        emb[index][i] = float(data[i])

features = np.hstack((emb, vertex_features))

path = '/Users/crescendo/Projects/DouyinDataAnalyse/data/label.npy'
labels = np.load(path)

X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=33)

print('data loaded')


model = GaussianNB()
model.fit(X_train, y_train)


print('model trained')

pred_test_y = model.predict(X_test)

precision = precision_score(y_test, pred_test_y)
print('precision: {}'.format(precision))
recall = recall_score(y_test, pred_test_y)
print('recall: {}'.format(recall))
f1_score = f1_score(y_test, pred_test_y)
print('f1 score: {}'.format(f1_score))
from sklearn.metrics import roc_curve, auc

fpr, tpr, th = roc_curve(y_test, pred_test_y, pos_label=1)
print('AUC: {}'.format(auc(fpr, tpr)))
score = model.score(X_test, y_test)
print('model score: {}'.format(score))
bg = sm.classification_report(y_test, pred_test_y)
print('分类报告：', bg, sep='\n')
pass
