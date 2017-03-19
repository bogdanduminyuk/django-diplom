# coding: utf-8


class CustomException(Exception):
    """Base class for all custom exceptions."""
    pass


class AdaptationTypeError(CustomException, TypeError):
    """Raised when got wrong type of adaptation."""
    def __init__(self, v_type):
        super(AdaptationTypeError, self).__init__('Type "' + v_type + '" not realized.')


class AdaptationVersionError(CustomException, ValueError):
    """Raised when got wrong version."""
    def __init__(self, cms_type, version):
        super(AdaptationVersionError, self).__init__("Version {0} of {1} is not realized".format(version, cms_type))
