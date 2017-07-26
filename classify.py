# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8');


import os
import fnmatch
from configure import BASE_DIR
from ppg.utils import make_dirs_for_file, exist, load_json, dump_json


splited_data_dir = os.path.join(BASE_DIR, 'data', 'splited')


if exist(pathname=splited_data_dir):
    for filename_with_ext in fnmatch.filter(os.listdir(splited_data_dir), '*.json'):
        pathname = os.path.join(splited_data_dir, filename_with_ext)
        json_data = load_json(pathname=pathname)
        if json_data is not None:
            pass
