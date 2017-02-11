# coding: utf-8
from adaptation import settings as adapt_settings


class WordPressAdapter:
    def __init__(self, description, data):
        self.description = description
        self.data = data

    def adapt(self):
        src_css = self.description['css']
        styles = self.get_wp_styles(src_css)
        return {'style.css': styles}

    def get_wp_styles(self, source_css_file):
        """
        Gets content of input css remade to wp.

        :param source_css_file: path to source css
        :return: wp css content
        """
        with open(source_css_file, 'r', encoding='utf-8') as styles_file:
            return adapt_settings.STYLES.format(
                self.data['name'],
                self.data.get('author', ''),
                self.data.get('description', ''),
                self.data['version'],
                self.data.get('theme_license', ''),
                self.data.get('tags', ''),
                self.data.get('comments', ''),
                styles_file.read()
            )

