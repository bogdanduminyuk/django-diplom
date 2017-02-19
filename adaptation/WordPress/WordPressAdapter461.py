# coding: utf-8
from bs4 import BeautifulSoup as bs

from adaptation.WordPress.WordPressAdapter import WordPressAdapter
from adaptation import settings as adapt_settings


class WordPressAdapter461(WordPressAdapter):
    """Custom wordpress adapter"""
    def adapt(self):
        files = {}

        contents = self.split_index()
        self.data.update(contents)

        for file, file_content in self.settings["FILES"].items():
            tpl_key = file + '.tpl'
            if tpl_key in self.templates:
                content = self.templates[tpl_key]['content'].format(**self.data)
            else:
                content = ''
                for starts, _content in contents.items():
                    if file.startswith(starts):
                        content = _content
                        break

            files[file] = file_content.format(content=content)

        for file, content in files.items():
            _content = content.replace('&lt;', '<')
            _content = _content.replace('&gt;', '>')
            files[file] = _content

        return files

    def split_index(self):
        header = self.page_parts['header']
        footer = self.page_parts['footer']
        content = self.index_content

        header_end_pos = content.find(header) + len(header)
        footer_start_pos = content.find(footer)

        header = content[0: header_end_pos]
        footer = content[footer_start_pos:]
        content = content[header_end_pos: footer_start_pos]

        return {
            "header": header,
            "index_content": content,
            "footer": footer,
        }
