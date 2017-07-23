# -*- coding: utf-8 -*-

from parameter import PPG_SAMPLE_RATE, PPG_FIR_TAP_NUM, PPG_FIR_CUTOFF


def smooth_ppg(signal, sample_rate=PPG_SAMPLE_RATE, numtaps=PPG_FIR_TAP_NUM, cutoff=PPG_FIR_CUTOFF):
    from scipy.signal import firwin, convolve
    if numtaps % 2 == 0:
        numtaps += 1
    return convolve(signal, firwin(numtaps, [x*2/sample_rate for x in cutoff], pass_zero=False), mode='valid')


def find_extrema(signal):
    import numpy as np
    from scipy.signal import argrelmax, argrelmin
    extrema_index = np.sort(np.unique(np.concatenate((argrelmax(signal)[0], argrelmin(signal)[0]))))
    extrema = signal[extrema_index]
    return zip(extrema_index.tolist(), extrema.tolist())


def validate_ppg(segment, sample_rate=PPG_SAMPLE_RATE):
    period = float(len(segment)) / float(sample_rate)
    if period < 0.5 or period > 1.2:
        return False
    import numpy as np
    max_index = np.argmax(segment)
    if float(max_index) / float(len(segment)) >= 0.5:
        return False
    from scipy.signal import argrelmax
    if len(argrelmax(np.array(segment))[0]) < 2:
        return False
    min_index = np.argmin(segment)
    if not (min_index == 0 or min_index == len(segment) - 1):
        return False
    diff = np.diff(segment[:max_index+1], n=1)
    if min(diff) < 0:
        return False
    if abs(segment[0] - segment[-1]) / (segment[max_index] - segment[min_index]) > 0.1:
        return False
    return True


def segment_ppg(signal, sample_rate=PPG_SAMPLE_RATE):
    threshold = (max(signal) - min(signal)) * 0.5
    segments = []
    last_extrema_index = None
    last_extrema = None
    last_segment_start_index = None
    for extrema_index, extrema in find_extrema(signal=signal):
        if last_extrema is not None and extrema - last_extrema > threshold:
            if last_segment_start_index is not None:
                segment = signal.tolist()[last_segment_start_index:last_extrema_index]
                if validate_ppg(segment=segment, sample_rate=sample_rate):
                    segments.append(segment)
            last_segment_start_index = last_extrema_index
        last_extrema_index = extrema_index
        last_extrema = extrema
    return segments