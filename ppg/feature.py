# -*- coding: utf-8 -*-

from parameter import PPG_SAMPLE_RATE


def scale(data):
    data_max = max(data)
    data_min = min(data)
    return [(x - data_min) / (data_max - data_min) for x in data]


def extract_svri(segment):
    import numpy as np
    max_index = np.argmax(segment)
    segment_scaled = scale(segment)
    return np.mean(segment_scaled[max_index:]) / np.mean(segment_scaled[:max_index])


def extract_ppg45(segment, sample_rate=PPG_SAMPLE_RATE):
    features = []
    import numpy as np
    from scipy.signal import argrelmax, argrelmin
    maxima_index = argrelmax(np.array(segment))[0]
    minima_index = argrelmin(np.array(segment))[0]
    segment_diff1 = np.diff(segment, n=1)
    maxima_index_diff1 = argrelmax(np.array(segment_diff1))[0]
    minima_index_diff1 = argrelmin(np.array(segment_diff1))[0]
    segment_diff2 = np.diff(segment, n=2)
    maxima_index_diff2 = argrelmax(np.array(segment_diff2))[0]
    minima_index_diff2 = argrelmin(np.array(segment_diff2))[0]
    # x
    x = segment[maxima_index[0]]
    features.append(x)
    # y
    y = segment[maxima_index[1]]
    features.append(y)
    # z
    z = segment[minima_index[0]]
    features.append(z)
    # t_pi
    t_pi = float(len(segment)) / float(sample_rate)
    features.append(t_pi)
    # y/x
    features.append(y / x)
    # (x-y)/x
    features.append((x - y) / x)
    # z/x
    features.append(z / x)
    # (y-z)/x
    features.append((y - z) / x)
    # t_1
    t_1 = float(maxima_index[0] + 1) / float(sample_rate)
    features.append(t_1)
    # t_2
    t_2 = float(minima_index[0] + 1) / float(sample_rate)
    features.append(t_2)
    # t_3
    t_3 = float(maxima_index[1] + 1) / float(sample_rate)
    features.append(t_3)
    # delta_t
    delta_t = t_3 - t_2
    features.append(delta_t)
    # width
    segment_halfmax = max(segment) / 2
    width = 0
    for value in segment[maxima_index[0]::-1]:
        if value >= segment_halfmax:
            width += 1
        else:
            break
    for value in segment[maxima_index[0]+1:]:
        if value >= segment_halfmax:
            width += 1
        else:
            break
    features.append(width)
    # A_2/A_1
    features.append(sum(segment[:maxima_index[0]]) / sum(segment[maxima_index[0]:]))
    # t_1/x
    features.append(t_1 / x)
    # y/(t_pi-t_3)
    features.append(y / (t_pi - t_3))
    # t_1/t_pi
    features.append(t_1 / t_pi)
    # t_2/t_pi
    features.append(t_2 / t_pi)
    # t_3/t_pi
    features.append(t_3 / t_pi)
    # delta_t/t_pi
    features.append(delta_t / t_pi)
    # t_a1
    t_a1 = float(maxima_index_diff1[0]) / float(sample_rate)
    features.append(t_a1)
    # t_b1
    t_b1 = float(minima_index_diff1[0]) / float(sample_rate)
    features.append(t_b1)
    # t_e1
    t_e1 = float(maxima_index_diff1[1]) / float(sample_rate)
    features.append(t_e1)
    # t_f1
    t_f1 = float(minima_index_diff1[1]) / float(sample_rate)
    features.append(t_f1)
    # b_2/a_2
    a_2 = segment_diff2[maxima_index_diff2[0]]
    b_2 = segment_diff2[minima_index_diff2[0]]
    features.append(b_2 / a_2)
    # e_2/a_2
    e_2 = segment_diff2[maxima_index_diff2[2]]
    features.append(e_2 / a_2)
    # (b_2+c_2)/a_2
    c_2 = segment_diff2[maxima_index_diff2[1]]
    features.append((b_2 + c_2) / a_2)
    # t_a2
    t_a2 = float(maxima_index_diff2[0]) / float(sample_rate)
    features.append(t_a2)
    # t_b2
    t_b2 = float(minima_index_diff2[0]) / float(sample_rate)
    features.append(t_b2)
    # t_a1/t_pi
    features.append(t_a1 / t_pi)
    # t_b1/t_pi
    features.append(t_b1 / t_pi)
    # t_e1/t_pi
    features.append(t_e1 / t_pi)
    # t_f1/t_pi
    features.append(t_f1 / t_pi)
    # t_a2/t_pi
    features.append(t_a2 / t_pi)
    # t_b2/t_pi
    features.append(t_b2 / t_pi)
    # (t_a1-t_a2)/t_pi
    features.append((t_a1 - t_a2) / t_pi)
    # (t_b1-t_b2)/t_pi
    features.append((t_b1 - t_b2) / t_pi)
    # (t_e1-t_2)/t_pi
    features.append((t_e1 - t_2) / t_pi)
    # (t_f1-t_3)/t_pi
    features.append((t_f1 - t_3) / t_pi)
    return features