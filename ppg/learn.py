# -*- coding: utf-8 -*-

import numpy as np
from sklearn import svm
from utils import flatten


def get_features_and_labels(data, task_levels, feature_types):
    train_features = []
    train_labels = []
    test_features = []
    test_labels = []
    for task_level in task_levels:
        for feature_type in feature_types:
            train_flattened_data, train_sample_num = flatten(blocks=data['train'][task_level], feature_types=feature_types)
            train_features.extend(train_flattened_data)
            train_labels.extend([task_level for x in range(train_sample_num)])
            test_flattened_data, test_sample_num = flatten(blocks=data['test'][task_level], feature_types=feature_types)
            test_features.extend(test_flattened_data)
            test_labels.extend([task_level for x in range(test_sample_num)])
    return train_features, train_labels, test_features, test_labels


def run_svm(data, task_levels, feature_types):
    train_features, train_labels, test_features, test_labels = get_features_and_labels(data, task_levels, feature_types)
    classifier = svm.SVC()
    classifier.fit(train_features, train_labels)
    return classifier.score(test_features, test_labels)