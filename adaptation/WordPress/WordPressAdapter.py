# coding: utf-8
from bs4 import BeautifulSoup as bs

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

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

    @staticmethod
    def prepare(content):
        """
        Prepares content using adapt_settings.

        :param content: page content
        :return: modified page content
        """
        soup = bs(content, 'html.parser')

        for method, attrs in adapt_settings.WORDPRESS['PREPARATION']['RELATIVES'].items():
            for attr, tags in attrs.items():
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

        return soup.prettify(formatter=None)
