#!/bin/bash

file=/Users/crescendo/Projects/developing/DouyinDataAnalyse/data/
train_file=/Users/crescendo/Projects/developing/DouyinDataAnalyse/src/net/deeprcmd/src/train.py

set -x
CUDA_VISIBLE_DEVICES=0 python -W ignore $train_file --tensorboard-log=exp \
    --model=gat --hidden-units=32,32 \
    --heads=4,4,1 --dim=64 --epochs=500 --lr=0.1 --dropout=0.2 --file-dir=$file \
    --batch=64 --train-ratio=75 --valid-ratio=12.5 \
    --instance-normalization --class-weight-balanced


# --use-vertex-feature