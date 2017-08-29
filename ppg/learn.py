# -*- coding: utf-8 -*-

from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier, VotingClassifier


def get_feature_set(data, level_set, feature_type_set):
    def __flatten(blocks, feature_type_set):
        flattened_data = []
        sample_num = 0
        for block in blocks:
            block_sample_num = len(block['ppg45'])
            flattened_block = [[] for x in range(block_sample_num)]
            for feature_type in feature_type_set:
                for sample_index in range(block_sample_num):
                    if isinstance(block[feature_type], list):
                        if isinstance(block[feature_type][0], list):
                            flattened_block[sample_index].extend(block[feature_type][sample_index])
                        else:
                            flattened_block[sample_index].append(block[feature_type][sample_index])
                    else:
                        flattened_block[sample_index].append(block[feature_type])
            flattened_data.extend(flattened_block)
            sample_num += block_sample_num
        return flattened_data, sample_num
    train_features = []
    train_labels = []
    test_features = []
    test_labels = []
    for level in level_set:
        for feature_type in feature_type_set:
            train_flattened_data, train_sample_num = __flatten(blocks=data['train'][level], feature_type_set=feature_type_set)
            train_features.extend(train_flattened_data)
            train_labels.extend([level for x in range(train_sample_num)])
            test_flattened_data, test_sample_num = __flatten(blocks=data['test'][level], feature_type_set=feature_type_set)
            test_features.extend(test_flattened_data)
            test_labels.extend([level for x in range(test_sample_num)])
    return train_features, train_labels, test_features, test_labels


def logistic_regression_classifier(features, labels):
    classifier = LogisticRegression(random_state=1)
    classifier.fit(features, labels)
    return classifier


def support_vector_classifier(features, labels):
    parameters = {
        'C': range(1, 101, 10),
        'kernel': ('linear', 'poly', 'rbf', 'sigmoid'),
    }
    classifier = GridSearchCV(SVC(random_state=1, probability=True), parameters, n_jobs=-1)
    classifier.fit(features, labels)
    return classifier


def gaussian_naive_bayes_classifier(features, labels):
    classifier = GaussianNB()
    classifier.fit(features, labels)
    return classifier


def decision_tree_classifier(features, labels):
    parameters = {
        'max_depth': [None] + range(1, 11, 1),
    }
    classifier = GridSearchCV(DecisionTreeClassifier(random_state=1), parameters, n_jobs=-1)
    classifier.fit(features, labels)
    return classifier


def random_forest_classifier(features, labels):
    parameters = {
        'n_estimators': range(10, 201, 10),
        'max_depth': [None] + range(1, 11, 1),
    }
    classifier = GridSearchCV(RandomForestClassifier(random_state=1), parameters, n_jobs=-1)
    classifier.fit(features, labels)
    return classifier


def adaboost_classifier(features, labels):
    parameters = {
        'n_estimators': range(50, 201, 10),
        'learning_rate': [float(x) / 10.0 for x in range(1, 11, 1)],
    }
    classifier = GridSearchCV(AdaBoostClassifier(random_state=1), parameters, n_jobs=-1)
    classifier.fit(features, labels)
    return classifier


def gradient_boosting_classifier(features, labels):
    parameters = {
        'learning_rate': [float(x) / 10.0 for x in range(1, 11, 1)],
        'n_estimators': range(50, 201, 10),
        'max_depth': range(1, 11, 1),
    }
    classifier = GridSearchCV(GradientBoostingClassifier(random_state=1), parameters, n_jobs=-1)
    classifier.fit(features, labels)
    return classifier


def voting_classifier(estimators, features, labels):
    parameters = {
        'voting': ['soft', 'hard'],
    }
    classifier = GridSearchCV(VotingClassifier(estimators=estimators), parameters, n_jobs=-1)
    classifier.fit(features, labels)
    return classifier