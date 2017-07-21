# -*- coding: utf-8 -*-

import sys


reload(sys)
sys.setdefaultencoding('utf-8');


import os
import fnmatch
import json
from config import BASE_DIR
from tools.common import make_dirs_for_file, exist_file


segmented_data_dir = os.path.join(BASE_DIR, 'data', 'segmented')


for filename_with_ext in fnmatch.filter(os.listdir(segmented_data_dir), '*.json'):
    print filename_with_ext