import os


def split_path(path):
    """Returns tuple of (folder, filename, ext) of given path"""
    _dir, _file = os.path.split(path)
    if _dir == '':
        _dir, _filename = _file, _dir
        _ext = ''
    else:
        _filename, _ext = os.path.splitext(_file)
    return _dir, _filename, _ext
