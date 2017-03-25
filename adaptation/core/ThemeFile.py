# coding: utf-8
from bs4 import BeautifulSoup as bs


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
            self.content = theme_file.read()
            self.soup = bs(self.content, "html.parser")
            return self.get_content()

    def write_content(self):
        """Writes content to new path"""
        content = self.get_content()
        with open(self.new_path, "w", encoding="utf-8") as theme_file:
            theme_file.write(content)

    def get_content(self):
        """Returns content converted from soup"""
        return str(self.soup).replace('&lt;', '<').replace('&gt;', '>')

    def prepare(self, method, getter):
        """
        Realizes applying of the method with getter as kwarg.

        :param method: method that will be applied
        :param getter: getter to get settings or something else
        :return: structure that method returns
        """
        prepared = method(self.content, {"getter": getter})
        self.content = prepared["content"]
        self.soup = bs(self.content, "html.parser")
        self.prepared = True
        return prepared

    # TODO: realize the method
    # TODO: move other file methods from getters.py
    def get_page_parts(self):
        pass
