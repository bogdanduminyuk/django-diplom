# coding: utf-8
from bs4 import BeautifulSoup as bs

from adaptation.WordPress.WordPressAdapter import WordPressAdapter
from adaptation import settings as adapt_settings


class WordPressAdapter461(WordPressAdapter):
    """Custom wordpress adapter"""
    def adapt(self):
        files = {}

        styles = self.get_wp_styles(self.description['css'])

        index = self.parse_index_file()

        files.update(styles)
        files.update(index)

        return files

    def parse_index_file(self):
        files = {}

        # TODO: add index
        with open(self.description['index'], 'r', encoding='utf-8') as index_file:
            content = index_file.read()

            content = self.prepare(content)

            for key, option in adapt_settings.WORDPRESS['INDEX'].items():
                filename = option['FILE']
                selector = option['SELECTOR']

                soup = bs(content, 'html.parser')
                sub_content = str(soup.select(selector)[0])
                position = content.find(sub_content)

                if key == 'HEADER':
                    sub_content = content[0:position] + sub_content
                elif key == 'FOOTER':
                    sub_content += content[position + len(sub_content)::]

                files[filename] = sub_content

            return files

