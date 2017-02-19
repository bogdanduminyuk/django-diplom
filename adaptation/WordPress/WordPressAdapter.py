# coding: utf-8
from bs4 import BeautifulSoup as bs
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

from adaptation.core.BaseAdapter import BaseAdapter


class WordPressAdapter(BaseAdapter):
    """Class keeps methods for all WordPress adapters"""
    def __init__(self, process_files, data):
        super(WordPressAdapter, self).__init__(process_files, data)

        preparation = self.settings.get("PREPARATION", False)

        if preparation:
            self.index_content = self.__do_preparation__(preparation, self.index_content)

        self.page_parts = self.__get_page_parts__(self.index_content)

    @staticmethod
    def __do_preparation__(preparation, content):
        """
        Prepares content using adapt_settings.

        :param content: page content
        :return: modified page content
        """
        methods = preparation['METHODS']
        soup = bs(content, "html.parser")

        for method, values in methods.items():
            for attr, tags in values.items():
                for tag in tags:
                    for tag_item in soup.find_all(tag):

                        validator = URLValidator()

                        try:
                            validator(tag_item.attrs[attr])
                        except ValidationError:
                            value = "<?php echo {0};?>/{1}".format(method, tag_item.attrs[attr])
                            tag_item.attrs[attr] = value
                        except KeyError:
                            pass

        return str(soup)
