# -*- coding: utf-8 -*-

import os


def get_base_dir():
    return os.path.abspath(os.path.dirname(__file__))


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
                print u'File: %s exists. Remove: overwrite old file.' % filename
            return False
        else:
            if display_info:
                print u'File: %s exists. Skip: no new file is created.' % filename
            return True
    else:
        if display_info:
            print u'File: %s does not exist. Create new file. ' % filename
        return False


def set_matplotlib_backend():
    import matplotlib
    if matplotlib.get_backend() == 'MacOSX':
        matplotlib.use('TkAgg')