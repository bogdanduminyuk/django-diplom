# coding: utf-8
from bs4 import BeautifulSoup as bs
from adaptation.core.adapters import BaseAdapter


class WordPressAdapter(BaseAdapter):
    """Class keeps methods for all WordPress adapters"""

    @staticmethod
    def prepare(file, **kwargs):
        super(WordPressAdapter, WordPressAdapter).prepare(file, **kwargs)

        for replacement in kwargs['settings']['REPLACEMENT']:
            part = file.get_page_part(replacement["page-part"])
            attrs = bs(part['content'], 'html.parser').contents[0].attrs
            params = replacement["params"].format(**{
                "menu_name": attrs["name"],
                "menu_class": ' '.join(attrs["class"]),
                "menu_id": attrs["id"]
            })
            file.replace(replacement["page-part"], replacement["template"].format(params=params))

        content = file.get_content()
        header = file.get_page_part('header')["content"]
        footer = file.get_page_part('footer')["content"]

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
