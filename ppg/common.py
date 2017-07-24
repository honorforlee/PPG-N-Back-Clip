# -*- coding: utf-8 -*-

import os
from json import load, dump


def make_dirs_for_file(filename):
    try:
        os.makedirs(os.path.split(filename)[0])
    except:
        pass


def exist_file(filename, overwrite=False, display_info=True):
    if os.path.exists(filename):
        if overwrite:
            os.remove(filename)
            if display_info:
                print u'File: %s exists. Overwrite.' % filename
            return False
        else:
            if display_info:
                print u'File: %s exists.' % filename
            return True
    else:
        if display_info:
            print u'File: %s does not exist.' % filename
        return False


def load_text(filename, display_info=True):
    if exist_file(filename, display_info=display_info):
        with open(filename, 'r') as f:
            return [line.strip() for line in f.readlines()]


def load_json(filename, display_info=True):
    if exist_file(filename, display_info=display_info):
        with open(filename, 'r') as f:
            return load(f)


def dump_json(data, filename, overwrite=False, display_info=True):
    make_dirs_for_file(filename)
    if not exist_file(filename, overwrite=overwrite, display_info=display_info):
        if display_info:
            print 'Write to file: %s' % filename
        with open(filename, 'w') as f:
            dump(data, f)


def parse_iso_time_string(timestamp):
    import dateutil.parser
    from dateutil import tz
    return dateutil.parser.parse(timestamp).astimezone(dateutil.tz.tzlocal()).replace(tzinfo=None)


def next_pow2(x):
    return 1<<(x-1).bit_length()


def scale(data):
    data_max = max(data)
    data_min = min(data)
    return [(x - data_min) / (data_max - data_min) for x in data]


def set_matplotlib_backend(backend=None):
    import matplotlib
    if matplotlib.get_backend() == 'MacOSX':
        matplotlib.use('TkAgg')
    if backend:
        matplotlib.use(backend)


def plot(args, backend=None):
    set_matplotlib_backend(backend=backend)
    import matplotlib.pyplot as plt
    plt.plot(*args)
    plt.show()