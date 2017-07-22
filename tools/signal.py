# -*- coding: utf-8 -*-


def smooth_ppg(signal, sample_rate=200, numtaps=200, cutoff=[0.5, 5.0]):
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


def validate_ppg(segment):
    return True


def segment_ppg(signal):
    threshold = (max(signal) - min(signal)) * 0.5
    segments = []
    last_extrema_index = None
    last_extrema = None
    last_segment_start_index = None
    for extrema_index, extrema in find_extrema(signal=signal):
        if last_extrema is not None and extrema - last_extrema > threshold:
            if last_segment_start_index is not None:
                segment = signal.tolist()[last_segment_start_index:last_extrema_index]
                if validate_ppg(segment=segment):
                    segments.append(segment)
            last_segment_start_index = last_extrema_index
        last_extrema_index = extrema_index
        last_extrema = extrema
    return segments
