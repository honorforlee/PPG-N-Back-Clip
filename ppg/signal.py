# -*- coding: utf-8 -*-

from parameter import PPG_SAMPLE_RATE, PPG_FIR_TAP_NUM, PPG_FIR_CUTOFF


def smooth_ppg_signal(signal, sample_rate=PPG_SAMPLE_RATE, numtaps=PPG_FIR_TAP_NUM, cutoff=PPG_FIR_CUTOFF):
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


def validate_ppg_single_waveform(single_waveform, sample_rate=PPG_SAMPLE_RATE):
    period = float(len(single_waveform)) / float(sample_rate)
    if period < 0.5 or period > 1.2:
        return False
    import numpy as np
    max_index = np.argmax(single_waveform)
    if float(max_index) / float(len(single_waveform)) >= 0.5:
        return False
    from scipy.signal import argrelmax
    if len(argrelmax(np.array(single_waveform))[0]) < 2:
        return False
    min_index = np.argmin(single_waveform)
    if not (min_index == 0 or min_index == len(single_waveform) - 1):
        return False
    diff = np.diff(single_waveform[:max_index+1], n=1)
    if min(diff) < 0:
        return False
    if abs(single_waveform[0] - single_waveform[-1]) / (single_waveform[max_index] - single_waveform[min_index]) > 0.1:
        return False
    return True


def extract_ppg_single_waveform(signal, sample_rate=PPG_SAMPLE_RATE):
    threshold = (max(signal) - min(signal)) * 0.5
    single_waveforms = []
    last_extrema_index = None
    last_extrema = None
    last_single_waveform_start_index = None
    for extrema_index, extrema in find_extrema(signal=signal):
        if last_extrema is not None and extrema - last_extrema > threshold:
            if last_single_waveform_start_index is not None:
                single_waveform = signal.tolist()[last_single_waveform_start_index:last_extrema_index]
                if validate_ppg_single_waveform(single_waveform=single_waveform, sample_rate=sample_rate):
                    single_waveforms.append(single_waveform)
            last_single_waveform_start_index = last_extrema_index
        last_extrema_index = extrema_index
        last_extrema = extrema
    return single_waveforms