#!/bin/bash

file=/Users/crescendo/Projects/developing/DouyinDataAnalyse/data/
train_file=/Users/crescendo/Projects/developing/DouyinDataAnalyse/src/net/deeprcmd/src/train.py

set -x
CUDA_VISIBLE_DEVICES=0 python -W ignore $train_file --tensorboard-log=exp \
    --model=pscn --file-dir=$file --epochs=1000 --dropout=0.2 \
    --dim=64 --lr=0.05 --hidden-units=16,8 --batch=64 \
    --train-ratio=75 --valid-ratio=12.5 --class-weight-balanced --instance-normalization \
    --neighbor-size=10 --sequence-size=16


# --use-vertex-feature
# K：neighbor-size
# W：sequence-size
