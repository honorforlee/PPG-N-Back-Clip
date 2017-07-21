# -*- coding: utf-8 -*-

import os


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
                print u'File: %s exists. Overwrite old file.' % filename
            return False
        else:
            if display_info:
                print u'File: %s exists.' % filename
            return True
    else:
        if display_info:
            print u'File: %s does not exist.' % filename
        return False


def parse_iso_time_string(timestamp):
    import dateutil.parser
    from dateutil import tz
    return dateutil.parser.parse(timestamp).astimezone(dateutil.tz.tzlocal()).replace(tzinfo=None)


def set_matplotlib_backend(backend=None):
    import matplotlib
    if matplotlib.get_backend() == 'MacOSX':
        matplotlib.use('TkAgg')
    if backend:
        matplotlib.use(backend)


def plot(x):
    import matplotlib.pyplot as plt
    plt.plot(x)
    plt.show()