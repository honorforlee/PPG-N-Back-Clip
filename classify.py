# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8');


import os
import fnmatch
from ppg import BASE_DIR
from ppg.utils import make_dirs_for_file, exist, load_json, dump_json
from ppg.learn import get_feature_set
from ppg.learn import logistic_regression_classifier
from ppg.learn import support_vector_classifier
from ppg.learn import gaussian_naive_bayes_classifier
from ppg.learn import decision_tree_classifier
from ppg.learn import random_forest_classifier, adaboost_classifier, gradient_boosting_classifier, voting_classifier


splited_data_dir = os.path.join(BASE_DIR, 'data', 'splited')


if exist(pathname=splited_data_dir):
    scores = []
    for filename_with_ext in fnmatch.filter(os.listdir(splited_data_dir), '*.json'):
        pathname = os.path.join(splited_data_dir, filename_with_ext)
        json_data = load_json(pathname=pathname)
        if json_data is not None:
            train_features, train_labels, test_features, test_labels = get_feature_set(data=json_data, task_levels=['0', '2'], feature_types=['ppg45_cr', 'svri_cr'])
            # score = logistic_regression_classifier(train_features, train_labels).score(test_features, test_labels)
            score = support_vector_classifier(train_features, train_labels).score(test_features, test_labels)
            # score = gaussian_naive_bayes_classifier(train_features, train_labels).score(test_features, test_labels)
            # score = decision_tree_classifier(train_features, train_labels).score(test_features, test_labels)
            # score = random_forest_classifier(train_features, train_labels).score(test_features, test_labels)
            # score = adaboost_classifier(train_features, train_labels).score(test_features, test_labels)
            # score = gradient_boosting_classifier(train_features, train_labels).score(test_features, test_labels)
            # score = voting_classifier(train_features, train_labels).score(test_features, test_labels)
            scores.append(score)
            print score
    print sum(scores) / len(scores)
