# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8');


import os
import fnmatch
import json
from configure import BASE_DIR
from ppg.common import make_dirs_for_file, exist_file, load_json, dump_json
from ppg.feature import extract_svri, extract_ppg45


preprocessed_data_dir = os.path.join(BASE_DIR, 'data', 'preprocessed')
extracted_data_dir = os.path.join(BASE_DIR, 'data', 'extracted')


for filename_with_ext in fnmatch.filter(os.listdir(preprocessed_data_dir), '*.json'):
    full_filename = os.path.join(preprocessed_data_dir, filename_with_ext)
    json_data = load_json(full_filename)
    if json_data is not None:
        for session_id in json_data:
            if json_data[session_id]['rest']['ppg']['segments'] is not None:
                json_data[session_id]['rest']['ppg']['svri'] = [extract_svri(segment) for segment in json_data[session_id]['rest']['ppg']['segments']]
                json_data[session_id]['rest']['ppg']['ppg45'] = [extract_ppg45(segment) for segment in json_data[session_id]['rest']['ppg']['segments']]
            else:
                json_data[session_id]['rest']['ppg']['svri'] = None
                json_data[session_id]['rest']['ppg']['ppg45'] = None
            del json_data[session_id]['rest']['ppg']['segments']
            for block in json_data[session_id]['blocks']:
                if block['ppg']['segments'] is not None:
                    block['ppg']['svri'] = [extract_svri(segment) for segment in block['ppg']['segments']]
                    block['ppg']['ppg45'] = [extract_ppg45(segment) for segment in block['ppg']['segments']]
                else:
                    block['ppg']['svri'] = None
                    block['ppg']['ppg45'] = None
                del block['ppg']['segments']
        full_output_filename = os.path.join(extracted_data_dir, filename_with_ext)
        dump_json(data=json_data, filename=full_output_filename, overwrite=True)