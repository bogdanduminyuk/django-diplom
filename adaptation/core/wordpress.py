# coding: utf-8


def adaptation_wordpress(src_dir, data):
    """
    Global WordPress adaptation method.

    Realizes checking for version and calls the appropriate adaptation method.
    Raises AdaptationVersionError if version can't be found.

    :param src_dir: path to the dir of unpacked input file
    :param data: data of input form and additional script data
    :return: dict {filename : content} to create on files_layer
    """
    def check_version(_version):
        # TODO: check for versions
        return _version

    version = check_version(data['version'])

    result = {
        "index.html": "<h1>wordpress</h1>"
    }

    return result
