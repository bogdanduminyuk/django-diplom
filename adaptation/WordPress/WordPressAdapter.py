# coding: utf-8

from adaptation.core.adapters import BaseAdapter


class WordPressAdapter(BaseAdapter):
    """Class keeps methods for all WordPress adapters"""

    @staticmethod
    def prepare(file, **kwargs):
        super(WordPressAdapter, WordPressAdapter).prepare(file, **kwargs)

        content = file.get_content()
        page_parts = file.get_page_parts()

        header = page_parts['header']
        footer = page_parts['footer']

        header_end_pos = content.find(header) + len(header)
        footer_start_pos = content.find(footer)

        header = content[0: header_end_pos]
        footer = content[footer_start_pos:]
        content = content[header_end_pos: footer_start_pos]

        kwargs["template_data"].update({
            "header": header,
            "footer": footer,
            "index_content": content,
        })
