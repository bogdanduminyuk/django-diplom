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

        # TODO: add copying of static files
        # TODO: simplify the code below
        with open(self.description['index'], 'r', encoding='utf-8') as index_file:
            content = index_file.read()
            content = self.prepare(content)

            soup = bs(content, 'html.parser')
            compressed_content = str(soup)

            for key, option in adapt_settings.WORDPRESS['INDEX'].items():
                filename = option['FILE']
                selector = option['SELECTOR']

                sub_content = str(soup.select(selector)[0])
                position = compressed_content.find(sub_content)

                if key == 'HEADER':
                    sub_content = compressed_content[0: position + len(sub_content)]
                elif key == 'FOOTER':
                    sub_content += compressed_content[position + len(sub_content):]

                compressed_content = compressed_content.replace(sub_content, "<?php " + option['METHOD_CALL'] + ";?>")
                files[filename] = sub_content

            files['index.php'] = compressed_content

            for file, content in files.items():
                content = content.replace('&lt;', '<')
                files[file] = content.replace('&gt;', '>')

            return files

