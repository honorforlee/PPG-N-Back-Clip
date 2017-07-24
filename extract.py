# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8');


import os
import fnmatch
from configure import BASE_DIR
from ppg.common import make_dirs_for_file, exist_file, load_json, dump_json
from ppg.feature import extract_ppg45, extract_svri
from ppg.feature import extract_mean_skin_conductance_level, extract_minimum_skin_conductance_level
from ppg.feature import extract_mean_rri, extract_rmssd


preprocessed_data_dir = os.path.join(BASE_DIR, 'data', 'preprocessed')
extracted_data_dir = os.path.join(BASE_DIR, 'data', 'extracted')


for filename_with_ext in fnmatch.filter(os.listdir(preprocessed_data_dir), '*.json'):
    full_filename = os.path.join(preprocessed_data_dir, filename_with_ext)
    json_data = load_json(full_filename)
    if json_data is not None:
        for session_id in json_data:
            if json_data[session_id]['rest']['ppg']['single_waveforms'] is not None:
                json_data[session_id]['rest']['ppg']['ppg45'] = [extract_ppg45(single_waveform=single_waveform, sample_rate=json_data[session_id]['rest']['ppg']['sample_rate']) for single_waveform in json_data[session_id]['rest']['ppg']['single_waveforms']]
                json_data[session_id]['rest']['ppg']['svri'] = [extract_svri(single_waveform=single_waveform) for single_waveform in json_data[session_id]['rest']['ppg']['single_waveforms']]
            else:
                json_data[session_id]['rest']['ppg']['ppg45'] = None
                json_data[session_id]['rest']['ppg']['svri'] = None
            del json_data[session_id]['rest']['ppg']['single_waveforms']
            if json_data[session_id]['rest']['skin_conductance']['signal'] is not None:
                json_data[session_id]['rest']['skin_conductance']['mean_level'] = extract_mean_skin_conductance_level(signal=json_data[session_id]['rest']['skin_conductance']['signal'])
                json_data[session_id]['rest']['skin_conductance']['minimum_level'] = extract_minimum_skin_conductance_level(signal=json_data[session_id]['rest']['skin_conductance']['signal'])
            else:
                json_data[session_id]['rest']['skin_conductance']['mean_level'] = None
                json_data[session_id]['rest']['skin_conductance']['minimum_level'] = None
            del json_data[session_id]['rest']['skin_conductance']['signal']
            if json_data[session_id]['rest']['ecg']['rri'] is not None:
                json_data[session_id]['rest']['ecg']['mean_rri'] = extract_mean_rri(rri=json_data[session_id]['rest']['ecg']['rri'])
                json_data[session_id]['rest']['ecg']['rmssd'] = extract_rmssd(rri=json_data[session_id]['rest']['ecg']['rri'])
            else:
                json_data[session_id]['rest']['ecg']['mean_rri'] = None
                json_data[session_id]['rest']['ecg']['rmssd'] = None
            del json_data[session_id]['rest']['ecg']['rri']
            for block in json_data[session_id]['blocks']:
                if block['ppg']['single_waveforms'] is not None:
                    block['ppg']['ppg45'] = [extract_ppg45(single_waveform=single_waveform, sample_rate=block['ppg']['sample_rate']) for single_waveform in block['ppg']['single_waveforms']]
                    block['ppg']['svri'] = [extract_svri(single_waveform=single_waveform) for single_waveform in block['ppg']['single_waveforms']]
                else:
                    block['ppg']['ppg45'] = None
                    block['ppg']['svri'] = None
                del block['ppg']['single_waveforms']
                if block['skin_conductance']['signal'] is not None:
                    block['skin_conductance']['mean_level'] = extract_mean_skin_conductance_level(signal=block['skin_conductance']['signal'])
                    block['skin_conductance']['minimum_level'] = extract_minimum_skin_conductance_level(signal=block['skin_conductance']['signal'])
                else:
                    block['skin_conductance']['mean_level'] = None
                    block['skin_conductance']['minimum_level'] = None
                del block['skin_conductance']['signal']
                if block['ecg']['rri'] is not None:
                    block['ecg']['mean_rri'] = extract_mean_rri(rri=block['ecg']['rri'])
                    block['ecg']['rmssd'] = extract_rmssd(rri=block['ecg']['rri'])
                else:
                    block['ecg']['mean_rri'] = None
                    block['ecg']['rmssd'] = None
                del block['ecg']['rri']
        full_output_filename = os.path.join(extracted_data_dir, filename_with_ext)
        dump_json(data=json_data, filename=full_output_filename, overwrite=True)