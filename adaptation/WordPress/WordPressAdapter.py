# coding: utf-8

from adaptation.core.adapters import BaseAdapter


class WordPressAdapter(BaseAdapter):
    """Class keeps methods for all WordPress adapters"""
    def __init__(self, getter, uploaded_files, request_data):
        super(WordPressAdapter, self).__init__(getter, uploaded_files, request_data)

    @staticmethod
    def preparation(content, **kwargs):
        result = super(WordPressAdapter, WordPressAdapter).preparation(content, **kwargs)
        content = self.prepared_files["index"]["content"]
        header = self.format_data['header']
        footer = self.format_data['footer']

        header_end_pos = content.find(header) + len(header)
        footer_start_pos = content.find(footer)

        header = content[0: header_end_pos]
        footer = content[footer_start_pos:]
        content = content[header_end_pos: footer_start_pos]
        return result

    def split_index(self):
        content = self.prepared_files["index"]["content"]
        header = self.format_data['header']
        footer = self.format_data['footer']

        header_end_pos = content.find(header) + len(header)
        footer_start_pos = content.find(footer)

        header = content[0: header_end_pos]
        footer = content[footer_start_pos:]
        content = content[header_end_pos: footer_start_pos]

        self.format_data.update({"header": header, "index_content": content, "footer": footer})
