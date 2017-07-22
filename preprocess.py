# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8');


import os
import fnmatch
import json
from configure import BASE_DIR
from ppg.common import make_dirs_for_file, exist_file, load_json, dump_json
from ppg.signal import smooth_ppg, segment_ppg


segmented_data_dir = os.path.join(BASE_DIR, 'data', 'segmented')
preprocessed_data_dir = os.path.join(BASE_DIR, 'data', 'preprocessed')


for filename_with_ext in fnmatch.filter(os.listdir(segmented_data_dir), '*.json'):
    full_filename = os.path.join(segmented_data_dir, filename_with_ext)
    json_data = load_json(full_filename)
    if json_data is not None:
        for session_id in json_data:
            if json_data[session_id]['rest']['ppg']['signal'] is not None:
                json_data[session_id]['rest']['ppg']['segments'] = segment_ppg(signal=smooth_ppg(signal=json_data[session_id]['rest']['ppg']['signal'], sample_rate=json_data[session_id]['rest']['ppg']['sample_rate']))
                del json_data[session_id]['rest']['ppg']['signal']
            for block in json_data[session_id]['blocks']:
                if block['ppg']['signal'] is not None:
                    block['ppg']['segments'] = segment_ppg(signal=smooth_ppg(signal=block['ppg']['signal'], sample_rate=block['ppg']['sample_rate']))
                    del block['ppg']['signal']
        full_output_filename = os.path.join(preprocessed_data_dir, filename_with_ext)
        dump_json(data=json_data, filename=full_output_filename, overwrite=True)