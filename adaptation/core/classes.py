# coding: utf-8


class CustomException(Exception):
    """Base class for all custom exceptions."""
    pass


class UserFileNotFoundError(CustomException, FileNotFoundError):
    """Raised when one of required files was not found."""
    def __init__(self, filename):
        super(UserFileNotFoundError, self).__init__(filename + ' not found but required.')


class DescriptionKeyNotFoundError(CustomException, KeyError):
    """Raised when key from description ini does not found."""
    def __init__(self, key):
        super(DescriptionKeyNotFoundError, self).__init__('Key "' + key + '" not found in description.json.')


class AdaptationTypeError(CustomException, TypeError):
    """Raised when got wrong type of adaptation."""
    def __init__(self, v_type):
        super(AdaptationTypeError, self).__init__('Type "' + v_type + '" not realized.')


class AdaptationVersionError(CustomException, ValueError):
    """Raised when got wrong version."""
    def __init__(self, version):
        super(AdaptationVersionError, self).__init__('Version "' + version + '" not realized.')
