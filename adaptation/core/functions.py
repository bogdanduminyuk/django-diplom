import os

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator


def split_path(path):
    """Returns tuple of (folder, filename, ext) of given path"""
    _dir, _file = os.path.split(path)
    if _dir == '':
        _dir, _filename = _file, _dir
        _ext = ''
    else:
        _filename, _ext = os.path.splitext(_file)
    return _dir, _filename, _ext


def is_url(string):
    """
    Checks if the string is url.

    :param string: string that can be url
    :return: True if string if url and False otherwise
    """
    validator = URLValidator()
    valid = True

    try:
        validator(string)
    except ValidationError:
        valid = False

    return valid
