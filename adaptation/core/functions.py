import os


def split_path(path):
    """Returns tuple of (folder, filename, ext) of given path"""
    _dir, _file = os.path.split(path)
    _filename, _ext = os.path.splitext(_file)
    return _dir, _filename, _ext
