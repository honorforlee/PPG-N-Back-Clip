# -*- coding: utf-8 -*-

import sys


reload(sys)
sys.setdefaultencoding('utf-8');


import os
import fnmatch
import json
from config import BASE_DIR
from tools.common import make_dirs_for_file, exist_file, set_matplotlib_backend, plot
from tools.signal import smooth_ppg, segment_ppg


segmented_data_dir = os.path.join(BASE_DIR, 'data', 'segmented')


for filename_with_ext in fnmatch.filter(os.listdir(segmented_data_dir), '*.json'):
    full_filename = os.path.join(segmented_data_dir, filename_with_ext)
    if exist_file(full_filename, display_info=True):
        with open(full_filename, 'r') as f:
            segmented_data = json.load(f)
            # print len(segmented_data['1']['blocks'][0]['ppg']['data'])
            # print len(smooth_ppg(segmented_data['1']['blocks'][0]['ppg']['data']))
            set_matplotlib_backend()
            # plot(segmented_data['1']['blocks'][0]['ppg']['data'])
            smoothed_ppg_data = smooth_ppg(signal=segmented_data['1']['blocks'][0]['ppg']['data'])
            import numpy as np
            print np.mean(smoothed_ppg_data)
            plot(smoothed_ppg_data)
    break
