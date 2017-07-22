# -*- coding: utf-8 -*-

from ..config import PPG_SAMPLE_RATE, PPG_FIR_TAP_NUM, PPG_FIR_CUTOFF


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
