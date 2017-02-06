# coding: utf-8
import os

from adaptation.core.classes import AdaptationVersionError
from adaptation import settings as adapt_settings


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
    user_description = data['description']

    name = data['name']
    author = data.get('author', '')
    description = data.get('description', '')
    version = data['version']
    theme_license = data.get('theme_license', '')
    tags = data.get('tags', '')
    comments = data.get('comments', '')

    styles_css = os.path.join(src_dir, user_description['css'])
    with open(styles_css, 'r', encoding='utf-8') as styles_file:
        styles_content = styles_file.read()
        # TODO: finish it
        adapt_styles_content = adapt_settings.STYLES.format(name, author, description, version, theme_license, tags, comments, styles_content)

    result = {
        "index.html": "<h1>wordpress</h1>"
    }

    return result
