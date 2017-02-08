# coding: utf-8

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
    def get_wp_styles_content(src_css_path, data):
        """
        Returns content of style's file.

        :param src_css_path: path to the dir of unpacked input file
        :param data: data of input form and additional script data
        :return:
        """
        with open(src_css_path, 'r', encoding='utf-8') as styles_file:
            return adapt_settings.STYLES.format(
                data['name'],
                data.get('author', ''),
                data.get('description', ''),
                data['version'],
                data.get('theme_license', ''),
                data.get('tags', ''),
                data.get('comments', ''),
                styles_file.read()
            )

    def handle_index_file(src_index_path, data):
        pass

    user_description = data['description.json']

    result = {
        "style.css": get_wp_styles_content(user_description['css'], data),
        "index.php": handle_index_file(user_description['index'], data)
    }

    return result
