#!/usr/bin/env python
# encoding: utf-8
# Author: Guangping ZHANG
# Create Time: 2020/01/25

import argparse
import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split


def load_data():
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

    features = (features - features.mean()) / features.std()
    # labels[np.where(labels == 0)] = -1

    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=33)
    return X_train, X_test, y_train, y_test


def train(X, Y, model, args):
    X = torch.FloatTensor(X)
    Y = torch.FloatTensor(Y)
    N = len(Y)

    optimizer = optim.SGD(model.parameters(), lr=args.lr)

    model.train()
    for epoch in range(args.epoch):
        perm = torch.randperm(N)
        sum_loss = 0

        for i in range(0, N, args.batchsize):
            x = X[perm[i : i + args.batchsize]].to(args.device)
            y = Y[perm[i : i + args.batchsize]].to(args.device)

            optimizer.zero_grad()
            output = model(x).squeeze()
            weight = model.weight.squeeze()

            loss = torch.mean(torch.clamp(1 - y * output, min=0))
            loss += args.c * (weight.t() @ weight) / 2.0

            loss.backward()
            optimizer.step()

            sum_loss += float(loss)

        print("Epoch: {:4d}\tloss: {}".format(epoch, sum_loss / N))


def visualize(X, Y, model):
    W = model.weight.squeeze().detach().cpu().numpy()
    b = model.bias.squeeze().detach().cpu().numpy()

    z = X.dot(W) + b

    delta = 0.001
    x = np.arange(X[:, 0].min(), X[:, 0].max(), delta)
    y = np.arange(X[:, 1].min(), X[:, 1].max(), delta)
    x, y = np.meshgrid(x, y)
    xy = list(map(np.ravel, [x, y]))

    z = (W.dot(xy) + b).reshape(x.shape)
    z[np.where(z > 1.0)] = 4
    z[np.where((z > 0.0) & (z <= 1.0))] = 3
    z[np.where((z > -1.0) & (z <= 0.0))] = 2
    z[np.where(z <= -1.0)] = 1

    plt.figure(figsize=(10, 10))
    plt.xlim([X[:, 0].min() + delta, X[:, 0].max() - delta])
    plt.ylim([X[:, 1].min() + delta, X[:, 1].max() - delta])
    plt.contourf(x, y, z, alpha=0.8, cmap="Greys")
    plt.scatter(x=X[:, 0], y=X[:, 1], c="black", s=10)
    plt.tight_layout()
    plt.show()


def eval(X, Y, model):
    X = torch.FloatTensor(X)
    Y = torch.FloatTensor(Y)
    y_pred = []
    for x in X:
        x = x.to(args.device)
        o = model(x)
        y_pred.append(o)
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--c", type=float, default=0.01)
    parser.add_argument("--lr", type=float, default=0.1)
    parser.add_argument("--batchsize", type=int, default=5)
    parser.add_argument("--epoch", type=int, default=10)
    parser.add_argument("--device", default="cpu", choices=["cpu", "cuda"])
    args = parser.parse_args()
    args.device = torch.device(args.device if torch.cuda.is_available() else "cpu")

    print(args)

    X_train, X_test, y_train, y_test = load_data()

    model = nn.Linear(81, 1)
    model.to(args.device)

    train(X_train, y_train, model, args)
    visualize(X_test, y_test, model)