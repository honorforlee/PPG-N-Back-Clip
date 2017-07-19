# -*- coding: utf-8 -*-

import sys


reload(sys)
sys.setdefaultencoding('utf-8');


import os
import fnmatch
import json
from common import BASE_DIR, make_dirs_for_file, exist_file


segmented_data_dir = os.path.join(BASE_DIR, 'data', 'segmented')