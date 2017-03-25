# coding: utf-8
from bs4 import BeautifulSoup as bs

from adaptation import settings as adapt_settings


class ThemeFile:
    def __init__(self, old_path, new_path):
        self.old_path = old_path
        self.new_path = new_path

        self.content = None
        self.soup = None
        self.prepared = False

    def read_content(self):
        """
        Reads content from old path. Creates soup object.

        :return: file content
        """
        with open(self.old_path, "r", encoding="utf-8") as theme_file:
            raw_content = theme_file.read()
            self.soup = bs(raw_content, "html.parser")
            self.content = self.get_content()
            return self.content

    def write_content(self):
        """Writes content to new path"""
        content = self.get_content()
        with open(self.new_path, "w", encoding="utf-8") as theme_file:
            theme_file.write(content)

    def get_content(self):
        """Returns content converted from soup"""
        return str(self.soup).replace('&lt;', '<').replace('&gt;', '>')

    def prepare(self, method, settings):
        """
        Realizes applying of the method with getter as kwarg.

        :param settings: dict described preparation settings
        :param method: method that will be applied
        :return: structure that method returns
        """
        prepared = method(self.content, settings=settings)
        self.soup = bs(self.content, "html.parser")
        self.content = self.get_content()
        self.prepared = True
        return prepared

    def get_page_parts(self):
        """
        Realizes selection using selectors.

        Uses PAGE_PARTS selectors.

        :return: dict <page_part : content>
        """
        parts = {}
        content = self.get_content()
        soup = bs(content, 'html.parser')

        for part, values in adapt_settings.PAGE_PARTS.items():
            selector = values["SELECTOR"]
            parts[part] = str(soup.select(selector)[0])

        return parts

    def get_page_elements(self):
        """
        Returns a dict of lists those contain tags.

        Tags are described in adapt_settings.PAGE_ELEMENTS.

        :return: dict of tags lists
        """
        soup = bs(self.content, "html.parser")
        elements = {}

        for page_element in adapt_settings.PAGE_ELEMENTS:
            elements_list = soup.select(page_element)
            elements[page_element] = elements_list

        return elements
