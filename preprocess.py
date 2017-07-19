# -*- coding: utf-8 -*-

from common import get_base_dir, set_matplotlib_backend

import numpy as np
from scipy import signal
set_matplotlib_backend()
import matplotlib.pyplot as plt
b, a = signal.iirfilter(17, [50, 200], rs=60, btype='band', analog=True, ftype='cheby2')
w, h = signal.freqs(b, a, 1000)
fig = plt.figure()
ax = fig.add_subplot(111)
ax.semilogx(w, 20 * np.log10(abs(h)))
ax.set_title('Chebyshev Type II bandpass frequency response')
ax.set_xlabel('Frequency [radians / second]')
ax.set_ylabel('Amplitude [dB]')
ax.axis((10, 1000, -100, 10))
ax.grid(which='both', axis='both')
plt.show()