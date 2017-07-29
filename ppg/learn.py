# -*- coding: utf-8 -*-

from sklearn import svm


def get_feature_set(data, task_levels, feature_types):
    def __flatten(blocks, feature_types):
        flattened_data = []
        sample_num = 0
        for block in blocks:
            block_sample_num = len(block['ppg45'])
            flattened_block = [[] for x in range(block_sample_num)]
            for feature_type in feature_types:
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
    for task_level in task_levels:
        for feature_type in feature_types:
            train_flattened_data, train_sample_num = __flatten(blocks=data['train'][task_level], feature_types=feature_types)
            train_features.extend(train_flattened_data)
            train_labels.extend([task_level for x in range(train_sample_num)])
            test_flattened_data, test_sample_num = __flatten(blocks=data['test'][task_level], feature_types=feature_types)
            test_features.extend(test_flattened_data)
            test_labels.extend([task_level for x in range(test_sample_num)])
    return train_features, train_labels, test_features, test_labels


def svm_classifier(train_features, train_labels):
    classifier = svm.SVC()
    classifier.fit(train_features, train_labels)
    return classifier