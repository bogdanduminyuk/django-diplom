# coding: utf-8
from bs4 import BeautifulSoup as bs

from adaptation.WordPress.WordPressAdapter import WordPressAdapter
from adaptation import settings as adapt_settings


class WordPressAdapter461(WordPressAdapter):
    """Custom wordpress adapter"""
    def adapt(self):
        super(WordPressAdapter461, self).adapt()
        files = {}

        contents = self.split_index()
        self.format_data.update(contents)

        for file, file_content in self.settings["FILES"].items():
            tpl_key = file + '.tpl'
            if tpl_key in self.templates:
                content = self.templates[tpl_key]['content'].format(**self.format_data)
            else:
                content = ''
                for starts, _content in contents.items():
                    if file.startswith(starts):
                        content = _content
                        break

            files[file] = file_content.format(**self.format_data)

        return files
