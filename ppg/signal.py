# -*- coding: utf-8 -*-

import numpy as np
from scipy.signal import argrelmax, argrelmin, firwin, convolve
from scipy.interpolate import interp1d
from parameter import MINIMUM_PULSE_CYCLE, MAXIMUM_PULSE_CYCLE
from parameter import PPG_SAMPLE_RATE, PPG_FIR_FILTER_TAP_NUM, PPG_FILTER_CUTOFF, PPG_SYSTOLIC_PEAK_DETECTION_THRESHOLD_COEFFICIENT
from parameter import ECG_R_PEAK_DETECTION_THRESHOLD


def find_extrema(signal):
    signal = np.array(signal)
    extrema_index = np.sort(np.unique(np.concatenate((argrelmax(signal)[0], argrelmin(signal)[0]))))
    extrema = signal[extrema_index]
    return zip(extrema_index.tolist(), extrema.tolist())


def smooth_ppg_signal(signal, sample_rate=PPG_SAMPLE_RATE, numtaps=PPG_FIR_FILTER_TAP_NUM, cutoff=PPG_FILTER_CUTOFF):
    if numtaps % 2 == 0:
        numtaps += 1
    return convolve(signal, firwin(numtaps, [x*2/sample_rate for x in cutoff], pass_zero=False), mode='valid').tolist()


def validate_ppg_single_waveform(single_waveform, sample_rate=PPG_SAMPLE_RATE):
    period = float(len(single_waveform)) / float(sample_rate)
    if period < MINIMUM_PULSE_CYCLE or period > MAXIMUM_PULSE_CYCLE:
        return False
    max_index = np.argmax(single_waveform)
    if float(max_index) / float(len(single_waveform)) >= 0.5:
        return False
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
    threshold = (max(signal) - min(signal)) * PPG_SYSTOLIC_PEAK_DETECTION_THRESHOLD_COEFFICIENT
    single_waveforms = []
    last_extremum_index = None
    last_extremum = None
    last_single_waveform_start_index = None
    for extremum_index, extremum in find_extrema(signal=signal):
        if last_extremum is not None and extremum - last_extremum > threshold:
            if last_single_waveform_start_index is not None:
                single_waveform = signal[last_single_waveform_start_index:last_extremum_index]
                if validate_ppg_single_waveform(single_waveform=single_waveform, sample_rate=sample_rate):
                    single_waveforms.append(single_waveform)
            last_single_waveform_start_index = last_extremum_index
        last_extremum_index = extremum_index
        last_extremum = extremum
    return single_waveforms


def extract_rri(signal, sample_rate):
    rri = []
    rri_time = []
    last_extremum_index = None
    last_extremum = None
    last_r_peak_index = None
    for extremum_index, extremum in find_extrema(signal=signal):
        if last_extremum is not None and extremum - last_extremum > ECG_R_PEAK_DETECTION_THRESHOLD:
            if last_r_peak_index is not None:
                interval = float(extremum_index - last_r_peak_index) / float(sample_rate)
                if interval >= MINIMUM_PULSE_CYCLE and interval <= MAXIMUM_PULSE_CYCLE:
                    rri.append(interval)
                    rri_time.append(float(extremum_index) / float(sample_rate))
            last_r_peak_index = extremum_index
        last_extremum_index = extremum_index
        last_extremum = extremum
    return rri, rri_time


def interpolate_rri(rri, rri_time, sample_rate):
    f = interp1d(rri_time, rri, kind='cubic')
    step = 1.0 / float(sample_rate)
    return f(np.arange(rri_time[0], rri_time[-1] - step, step)).tolist()