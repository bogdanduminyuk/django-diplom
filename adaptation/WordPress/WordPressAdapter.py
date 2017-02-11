# coding: utf-8
from adaptation import settings as adapt_settings


class WordPressAdapter:
    @staticmethod
    def get_wp_styles(source_css_file, data):
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

