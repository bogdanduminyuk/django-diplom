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
    def get_wp_styles_content(src_dir, data):
        """
        Returns content of style's file.

        :param src_dir: path to the dir of unpacked input file
        :param data: data of input form and additional script data
        :return:
        """
        src_styles_path = os.path.join(src_dir, data['description']['css'])
        with open(src_styles_path, 'r', encoding='utf-8') as styles_file:
            return src_styles_path, adapt_settings.STYLES.format(
                data['name'],
                data.get('author', ''),
                data.get('description', ''),
                data['version'],
                data.get('theme_license', ''),
                data.get('tags', ''),
                data.get('comments', ''),
                styles_file.read()
            )

    css_path, css_content = get_wp_styles_content(src_dir, data)

    result = {
        css_path: get_wp_styles_content(src_dir, data),
        "index.html": "<h1>wordpress</h1>"
    }

    return result
