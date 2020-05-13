#!/bin/bash

file=/Users/crescendo/Projects/developing/DouyinDataAnalyse/data/
train_file=/Users/crescendo/Projects/developing/DouyinDataAnalyse/src/net/deeprcmd/src/train.py

set -x
CUDA_VISIBLE_DEVICES=0 python $train_file --tensorboard-log=exp \
    --model=gcn --hidden-units=128,128 \
    --dim=64 --epochs=500 --lr=0.1 --dropout=0.2 --file-dir=$file \
    --batch=64 --train-ratio=75 --valid-ratio=12.5 \
    --class-weight-balanced --instance-normalization --use-vertex-feature

