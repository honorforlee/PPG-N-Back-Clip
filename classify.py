# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8');


import os
import fnmatch
from ppg import BASE_DIR
from ppg.utils import make_dirs_for_file, exist, load_json, dump_json, load_model, dump_model
from ppg.learn import get_feature_set
from ppg.learn import logistic_regression_classifier
from ppg.learn import support_vector_classifier
from ppg.learn import gaussian_naive_bayes_classifier
from ppg.learn import decision_tree_classifier
from ppg.learn import random_forest_classifier, adaboost_classifier, gradient_boosting_classifier
from ppg.learn import voting_classifier


def classify():
    splited_data_dir = os.path.join(BASE_DIR, 'data', 'splited')
    model_dir = os.path.join(BASE_DIR, 'models')


    level_sets = [
        ['0', '2'],
        ['0', '1'],
        ['1', '2'],
    ]
    feature_type_sets = [
        ['ppg45_cr'],
        ['svri_cr'],
        ['ppg45_cr', 'svri_cr'],
        ['average_skin_conductance_level_cr', 'minimum_skin_conductance_level_cr'],
        ['average_rri_cr', 'rmssd_cr', 'mf_hrv_power_cr', 'hf_hrv_power_cr'],
    ]
    classifiers = [
        ('logistic_regression', logistic_regression_classifier, ),
        ('support_vector', support_vector_classifier, ),
        ('gaussian_naive_bayes', gaussian_naive_bayes_classifier, ),
        ('decision_tree', decision_tree_classifier, ),
        ('random_forest', random_forest_classifier, ),
        ('adaboost', adaboost_classifier, ),
        ('gradient_boosting', gradient_boosting_classifier, ),
        ('voting', voting_classifier, ),
    ]


    if exist(pathname=splited_data_dir):
        for filename_with_ext in fnmatch.filter(os.listdir(splited_data_dir), '*.json'):
            participant = os.path.splitext(filename_with_ext)[0]
            pathname = os.path.join(splited_data_dir, filename_with_ext)
            json_data = load_json(pathname=pathname)
            if json_data is not None:
                for level_set in level_sets:
                    for feature_type_set in feature_type_sets:
                        train_features, train_labels, test_features, test_labels = get_feature_set(data=json_data, level_set=level_set, feature_type_set=feature_type_set)
                        estimators = []
                        for classifier_name, classifier_object in classifiers:
                            model_pathname = os.path.join(model_dir, '-'.join(level_set), '-'.join(feature_type_set), classifier_name, '%s.model' % participant)
                            classifier = load_model(pathname=model_pathname)
                            if classifier is None:
                                if classifier_name == 'voting':
                                    classifier = classifier_object(estimators=estimators, features=train_features, labels=train_labels)
                                else:
                                    classifier = classifier_object(features=train_features, labels=train_labels)
                                make_dirs_for_file(pathname=model_pathname)
                                dump_model(model=classifier, pathname=model_pathname)
                            score = classifier.score(test_features, test_labels)
                            if classifier_name != 'voting':
                                if hasattr(classifier, 'best_estimator_'):
                                    estimators.append((classifier_name, classifier.best_estimator_, ))
                                else:
                                    estimators.append((classifier_name, classifier, ))
                            print participant, score, '-'.join(level_set), '-'.join(feature_type_set), classifier_name


if __name__ == '__main__':
    classify()