# coding: utf-8
from adaptation import settings as adapt_settings


class WordPressAdapter:
    def __init__(self, description, data):
        self.description = description
        self.data = data

    def adapt(self):
        src_css = self.description['css']
        styles = self.get_wp_styles(src_css, self.data)
        return {'style.css': styles}

    @staticmethod
    def get_wp_styles(source_css_file, data):
        """
        Gets content of input css remade to wp.

        :param source_css_file: path to source css
        :param data: form data
        :return: wp css content
        """
        with open(source_css_file, 'r', encoding='utf-8') as styles_file:
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

