# coding: utf-8
from adaptation import settings as adapt_settings
from adaptation.core.adapter import BaseAdapter


class WordPressAdapter(BaseAdapter):
    """Class keeps methods for all WordPress adapters"""
    def get_wp_styles(self, source_css_file):
        """
        Gets content of input css remade to wp.

        :param source_css_file: path to source css
        :return: wp css content
        """
        with open(source_css_file, 'r', encoding='utf-8') as styles_file:
            content = adapt_settings.WORDPRESS['STYLE']['CONTENT'].format(
                self.data['name'],
                self.data.get('author', ''),
                self.data.get('description', ''),
                self.data['version'],
                self.data.get('theme_license', ''),
                self.data.get('tags', ''),
                self.data.get('comments', ''),
                styles_file.read()
            )

            return {adapt_settings.WORDPRESS['STYLE']['FILE']: content}
