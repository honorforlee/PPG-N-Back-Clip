# -*- coding: utf-8 -*-


def plot(signal):
    import matplotlib.pyplot as plt
    plt.plot(signal)
    plt.show()


def smooth_ppg(signal, sample_rate=200, numtaps=200, cutoff=[0.5, 5.0]):
    from scipy.signal import firwin, convolve
    if numtaps % 2 == 0:
        numtaps += 1
    return convolve(signal, firwin(numtaps, [x*2/sample_rate for x in cutoff], pass_zero=False), mode='valid')
