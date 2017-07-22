# -*- coding: utf-8 -*-


def extract_svri(segment):
    import numpy as np
    max_index = np.argmax(segment)
    from sklearn import preprocessing
    min_max_scaler = preprocessing.MinMaxScaler()
    segment_minmax = min_max_scaler.fit_transform(segment)
    return np.mean(segment[max_index:]) / np.mean(segment[:max_index])


def extract_ppg45(segment):
    return