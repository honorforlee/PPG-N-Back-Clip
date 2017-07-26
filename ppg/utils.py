# -*- coding: utf-8 -*-

import os
from json import load, dump


def path_type(pathname):
    if os.path.isfile(pathname):
        return 'File'
    if os.path.isdir(pathname):
        return 'Directory'
    if os.path.islink(pathname):
        return 'Symbolic Link'
    if os.path.ismount(pathname):
        return 'Mount Point'
    return 'Path'


def make_dirs_for_file(pathname):
    try:
        os.makedirs(os.path.split(pathname)[0])
    except:
        pass


def exist(pathname, overwrite=False, display_info=True):
    if os.path.exists(pathname):
        if overwrite:
            if display_info:
                print u'%s: %s exists. Overwrite.' % (path_type(pathname), pathname)
            os.remove(pathname)
            return False
        else:
            if display_info:
                print u'%s: %s exists.' % (path_type(pathname), pathname)
            return True
    else:
        if display_info:
            print u'%s: %s does not exist.' % (path_type(pathname), pathname)
        return False


def load_text(pathname, display_info=True):
    if exist(pathname=pathname, display_info=display_info):
        with open(pathname, 'r') as f:
            return [line.strip() for line in f.readlines()]


def load_json(pathname, display_info=True):
    if exist(pathname=pathname, display_info=display_info):
        with open(pathname, 'r') as f:
            return load(f)


def dump_json(data, pathname, overwrite=False, display_info=True):
    make_dirs_for_file(pathname)
    if not exist(pathname=pathname, overwrite=overwrite, display_info=display_info):
        if display_info:
            print 'Write to file: %s' % pathname
        with open(pathname, 'w') as f:
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


def get_change_ratio(data, baseline):
    def change_ratio(value, baseline):
        return (value - baseline) / baseline
    if isinstance(baseline, list):
        import numpy as np
        baseline = np.mean(baseline, axis=0)
        return [change_ratio(value=value, baseline=baseline).tolist() for value in data]
    return change_ratio(value=data, baseline=baseline)


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


def semilogy(args, backend=None):
    set_matplotlib_backend(backend=backend)
    import matplotlib.pyplot as plt
    plt.semilogy(*args)
    plt.show()