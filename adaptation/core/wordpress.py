# coding: utf-8
from adaptation.core.classes import AdaptationVersionError


def adaptation_wordpress(src_dir, data):
    """
    Global WordPress adaptation method.

    Realizes checking for version and calls the appropriate adaptation method.
    Raises AdaptationVersionError if version can't be found.

    :param src_dir: path to the dir of unpacked input file
    :param data: data of input form and additional script data
    :return: dict {filename : content} to create on files_layer
    """
    version = data['version']

    if version == 461:
        call = adaptation_wordpress_461
    else:
        raise AdaptationVersionError("WordPress", version)

    return call(src_dir, data)


def adaptation_wordpress_461(src_dir, data):
    """
    WordPress 4.6.1 adaptation method.

    Realizes adaptation for wordpress v4.6.1.

    :param src_dir: path to the dir of unpacked input file
    :param data: data of input form and additional script data
    :return: dict {filename : content} to create on files_layer
    """

    return {
        "index.html": "<h1>wordpress</h1>"
    }
