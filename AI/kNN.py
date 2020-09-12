#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  @Product: PyCharm
#  @Project: python
#  @File    : kNN.py
#  @Author  : big
#  @Email   : shdorado@126.com
#  @Time    : 2020/7/2 12:42
#  功能：


import sys
import numpy as np
import operator


def create_data_set():
    group = np.array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels


def classifyO(inX, dataset, labels, k):
    dataSetSize = dataset.shape[0]
    diffMat = np.tile(inX, (dataSetSize, 1)) - dataset
    # print(np.tile(inX, (dataSetSize, 1)), dataset, diffMat)
    sqDiffMat = diffMat ** 2

    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances ** 0.5
    sortedDistindicies = distances.argsort()
    classCount = {}
    for i in range(k):
        voteilabel = labels[sortedDistindicies[i]]
        classCount[voteilabel] = classCount.get(voteilabel, 0) + 1
    sortedClassCount = sorted(classCount.items(),
                              key=operator.itemgetter(1), reverse=True)

    return sortedClassCount[0][0]


def main():
    group, labels = create_data_set()
    print(group, labels)
    label = classifyO([0, 0], group, labels, 3)
    print(label)
    # print(group, group[0, 2:3], group[2::2, ::2])


if __name__ == '__main__':
    main()
