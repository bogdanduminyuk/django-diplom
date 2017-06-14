import os
import shutil
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

from bs4 import BeautifulSoup

from adaptation import settings as adapt_settings
from base import settings as base_settings


class FileSystemObject:
    """Class is base for objects of file system (files, directories)."""
    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)

    def copy(self, wpath):
        pass


class DirectoryObject(FileSystemObject):
    """Class is base for directories"""
    def __init__(self, path):
        super().__init__(path)

    def copy(self, wpath):
        """Copies directory from rpath to wpath"""
        shutil.copytree(self.path, os.path.join(wpath, self.name))


class FileObject(FileSystemObject):
    """Global file object used as base file"""
    def __init__(self, path):
        super().__init__(path)
        self.directory = os.path.dirname(path)
        self.extension = os.path.splitext(path)[1]

    def copy(self, wpath):
        """Copies file from rpath to wpath"""
        shutil.copyfile(self.path, os.path.join(wpath, self.name))

    def get_content(self):
        """Returns content of file using self.path."""
        with open(self.path, 'r', encoding='utf-8') as file:
            return file.read()

    def put_content(self, content, path=None):
        """Simple file writing."""
        path = self.path if path is None else path

        with open(path, 'w', encoding='utf-8') as file:
            file.write(content)


class TemplateFile(FileObject):
    """Class realizes TemplateFile that used with adapters."""
    def __init__(self, path):
        super().__init__(path)
        self.template_file_name = os.path.splitext(os.path.basename(path))[0]

    def get_template(self, **kwargs):
        """Realizes applying template keys to its content."""
        return self.get_content().format(**kwargs) if kwargs else self.get_content()


class XMLFile(FileObject):
    """Realizes working with xml files. Represents one xml file."""
    def __init__(self, path, root_name, attributes=None):
        super().__init__(path)
        self.root = ET.Element(root_name)
        self.__add_attributes__(self.root, attributes)

    def put_content(self):
        """Writes xml to file."""
        content = self.get_content()
        super().put_content(content)

    def add_child(self, append_to, name, text="", attributes=None):
        """
        Creates and append child to append_to_element.

        :param append_to: xpath for element where to append
        :param name: name of new element
        :param text: text of new element
        :param attributes: attributes of new element
        :return: None
        """
        parent = self.root.find(append_to)
        sub_element = ET.SubElement(parent, name)
        sub_element.text = str(text)
        self.__add_attributes__(sub_element, attributes)

    def get_content(self):
        """
        Returns pretty xml of self.base_element.

        :return: pretty xml string
        """
        rough_string = ET.tostring(self.root, encoding='utf-8', method='xml')
        re_parsed = minidom.parseString(rough_string)
        return re_parsed.toprettyxml(indent=4 * ' ', encoding='utf-8').decode('utf-8')

    @staticmethod
    def __add_attributes__(element, attributes):
        """
        Adds attributes to the element.

        :param element: XML-element
        :param attributes: dict of attributes <attr : value>
        """
        if attributes is not None:
            for attribute, value in attributes.items():
                element.set(attribute, str(value))


class ParsableFile(FileObject):
    """
    Class of parsed theme files.

    Uses all files that should be parsed from src dir.
    """
    def __init__(self, path):
        super().__init__(path)
        self.soup = None

    def read(self):
        """Initializes soup as file content."""
        content = super().get_content()
        self.soup = BeautifulSoup(content, "html.parser")

    def get_content(self, formatter=None):
        """Returns content converted from soup."""
        return self.soup.prettify(formatter=formatter) if formatter != 'str' else str(self.soup)

    def select(self, selector, as_string=False):
        """Realizes simple selection from soup."""
        selection = self.soup.select(selector)
        return [str(i) for i in selection] if as_string else selection

    def get_page_parts(self, *parts, as_string=True):
        """
        Returns dict of <page_part: selection> by given keys.

        If keys is False returns  the same dict constructed from all page parts.

        :param as_string: 
        :param parts: tuple of string keys
        :return: dict
        """
        intersection = set(parts) & adapt_settings.PAGE_PARTS.keys()
        keys = intersection if intersection else adapt_settings.PAGE_PARTS.keys()

        return {
            key: self.select(value["SELECTOR"], as_string=as_string)
            for key, value in adapt_settings.PAGE_PARTS.items() if key in keys
        }

    def get_page_tags(self, *tags, parent=""):
        """
        Realizes getting tags info and selection.

        If tags does not given then method uses all tags the system knows.
        If parent does not given the selection search globally otherwise it uses 'parent tag_name' selector.

        :param tags: tuple of tags
        :param parent: parent selector e.g. 'body script'
        :return: dict <tag_name: <"selection":selection, "info":info> >
        """
        intersection = set(tags) & base_settings.TAGS.keys()
        keys = intersection if intersection else base_settings.TAGS.keys()

        return {
            tag_name: {
                "selection": self.select(parent + " " + tag_name if parent else tag_name, False),
                "info": data
            }
            for tag_name, data in base_settings.TAGS.items() if tag_name in keys
        }
