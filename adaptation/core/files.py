# coding: utf-8
import os
from abc import ABCMeta, abstractmethod

from bs4 import BeautifulSoup as bs

from adaptation import settings as adapt_settings


class ReadableFile(metaclass=ABCMeta):
    """Abstract class for Readable files. It used in File-object inheritance."""
    def __init__(self, rpath):
        self.rpath = rpath

    def read(self):
        """Get content from file using rpath"""
        with open(self.rpath, "r", encoding="utf-8") as file:
            return file.read()

    @abstractmethod
    def get_content(self, **kwargs):
        pass


class WritableFile(metaclass=ABCMeta):
    """Abstract class for Writable files. It used in File-object inheritance."""
    def __init__(self, wpath):
        self.wpath = wpath

    @abstractmethod
    def write(self, content):
        """Writes content to wpath"""
        with open(self.wpath, "w", encoding="utf-8") as file:
            file.write(content)


class ReadableWritableFile(ReadableFile, WritableFile, metaclass=ABCMeta):
    """Abstract class for ReadableWritable files. It used in File-object inheritance."""
    def __init__(self, rpath, wpath):
        ReadableFile.__init__(self, rpath)
        WritableFile.__init__(self, wpath)
        self.content = None

    def read(self):
        """Keeps content in class property"""
        self.content = super().read()

    def write(self, content=""):
        """Writes content to wpath. Uses object property if it is not given."""
        if not content:
            content = self.get_content()
        super().write(content)


class TemplateFile(ReadableFile):
    """Class realizes TemplateFile that used with adapters."""
    def __init__(self, template_path):
        super(TemplateFile, self).__init__(template_path)
        self.name = os.path.basename(template_path)

    def get_content(self, **kwargs):
        """Realizes applying template keys to its content."""
        return self.read().format(**kwargs) if kwargs else self.read()


class ThemeFile(ReadableWritableFile):
    def __init__(self, old_path, new_path):
        super().__init__(old_path, new_path)
        self.soup = None
        self.prepared = False

    def read(self):
        super().read()
        self.soup = bs(self.content, "html.parser")

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
        self.prepared = method(self.content, settings=settings)
        self.soup = bs(self.content, "html.parser")
        self.content = self.get_content()
        return self.prepared

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

if __name__ == "__main__":
    classes = [ReadableFile, WritableFile, ReadableWritableFile, TemplateFile, ThemeFile]
    params = [
        ("rpath",),
        ("wpath",),
        ("rpath", "wpath"),
        ("rpath",),
        ("rpath", "wpath"),
    ]

    for CreateClass, parameters in zip(classes, params):
        try:
            var = CreateClass(*parameters)
        except TypeError as e:
            print(e)
        else:
            try:
                print(var.rpath)
            except AttributeError as e:
                print(e)

            try:
                print(var.wpath)
            except AttributeError as e:
                print(e)

    tpl_file = TemplateFile(r"E:\git-workspace\diplom\adaptation\WordPress\static\tpl\style.css.tpl")
    print(tpl_file.get_content())
    try:
        print(tpl_file.get_content(name="name"))
    except KeyError as e:
        print("Key does not exist:", e)
    print("tpl_file name:", tpl_file.name)

    theme_file = ThemeFile(r"E:\git-workspace\diplom\tmp\snowboarding\index.html",
                           r"E:\git-workspace\diplom\tmp\uploads\snowboarding\index.html")
    theme_file.read()
    theme_file.write()


