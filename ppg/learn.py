# -*- coding: utf-8 -*-

from sklearn import svm


def svm(train_features, train_labels, test_features, test_labels):
    classifier = svm.SVC()
    classifier.fit(train_features, train_labels)
    return classifier.score(test_features, test_labels)