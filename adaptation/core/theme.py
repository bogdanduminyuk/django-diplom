# coding: utf-8
import os

# TODO: remove after testing
os.environ['DJANGO_SETTINGS_MODULE'] = 'diplom.settings'

import shutil
import xml.dom.minidom as minidom
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup as bs

from adaptation import settings as adapt_settings
from diplom import settings


class FileSystemObject:
    """Class is base for objects of file system (files, directories)."""
    def __init__(self, rpath, wpath):
        self.rpath = rpath
        self.wpath = wpath


class DirectoryObject(FileSystemObject):
    """Class is base for directories"""
    def copy(self):
        """Copies directory from rpath to wpath"""
        shutil.copytree(self.rpath, self.wpath)


class FileObject(FileSystemObject):
    """Global file object used as base file"""
    def __init__(self, rpath, wpath):
        super().__init__(rpath, wpath)
        self.content = ""

    def read(self):
        """Simple file reading."""
        if self.rpath:
            with open(self.rpath, "r", encoding="utf-8") as file:
                self.content = file.read()
                return self.content

    def write(self):
        """Simple file writting."""
        if self.wpath:
            with open(self.wpath, "w", encoding="utf-8") as file:
                file.write(self.content)

    def get_content(self, **kwargs):
        return self.content


class TemplateFile(FileObject):
    """Class realizes TemplateFile that used with adapters."""
    def __init__(self, template_path):
        super(TemplateFile, self).__init__(template_path, "")

    def get_content(self, **kwargs):
        """Realizes applying template keys to its content."""
        return self.read().format(**kwargs) if kwargs else self.read()


class XMLFile(FileObject):
    """Realizes working with xml files. Represents one xml file."""
    def __init__(self, rpath, wpath, main_element_name, attributes=None):
        super(XMLFile, self).__init__(rpath, wpath)
        self.base_element = ET.Element(main_element_name)
        self.__add_attributes__(self.base_element, attributes)

    def read(self):
        """Reads xml content from file."""
        tree = ET.parse(self.rpath)
        self.base_element = tree.getroot()

    def write(self):
        """Writes xml to file."""
        if not self.content:
            self.content = self.get_content()
        super().write()

    def add_child(self, append_to, name, text="", attributes=None):
        """
        Creates and append child to append_to_element.

        :param append_to: xpath for element where to append
        :param name: name of new element
        :param text: text of new element
        :param attributes: attributes of new element
        :return: None
        """
        parent = self.base_element.find(append_to)
        sub_element = ET.SubElement(parent, name)
        sub_element.text = str(text)
        self.__add_attributes__(sub_element, attributes)

    def get_content(self, **kwargs):
        """
        Returns pretty xml of self.base_element.

        :return: pretty xml string
        """
        rough_string = ET.tostring(self.base_element, encoding='utf-8', method='xml')
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


class ThemeFile(FileObject):
    """Base theme file."""
    def __init__(self, old_path, new_path):
        super().__init__(old_path, new_path)
        self.filename = os.path.basename(old_path)


class NewThemeFile(ThemeFile):
    """
    Simple file than should not be parsed.

    It should be just moved.
    """
    def __init__(self, new_path):
        super().__init__("", new_path)
        del self.rpath


class ParsedThemeFile(ThemeFile):
    """
    Class of parsed theme files.

    Uses all files that should be parsed from src dir.
    """
    def __init__(self, old_path, new_path):
        super().__init__(old_path, new_path)
        self.prepared = False
        self.soup = None

    def read(self):
        """Initializes soup as file content."""
        super().read()
        self.soup = bs(self.content, "html.parser")

    def write(self):
        self.content = self.get_content()
        super().write()

    def get_content(self, **kwargs):
        """Returns content converted from soup."""
        return str(self.soup).replace('&lt;', '<').replace('&gt;', '>')

    def set_content(self, content):
        """Sets content param as current content."""
        self.soup = bs(content, "html.parser")
        self.content = self.get_content()

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


class Theme:
    def __init__(self, src_zip, src_dir, dst_dir, name):
        self.src_zip = src_zip
        self.src_dir = src_dir
        self.dst_dir = dst_dir
        self.name = name
        self.is_unpacked = False
        self.is_written = False

        self.dirs = []
        self.src_files = {}
        self.dst_files = []

    def unpack(self):
        """Realizes unpacking of the theme archive to src_dir folder."""
        shutil.unpack_archive(self.src_zip, self.src_dir, 'zip')
        self.is_unpacked = True
        return self.src_dir

    def pack(self):
        """Realizes packing of the dst_dir folder."""
        if not self.is_written:
            self.write_files()

        path = shutil.make_archive(self.dst_dir, 'zip', root_dir=settings.MEDIA_ROOT, base_dir=self.name)
        return os.path.join(settings.MEDIA_URL, os.path.basename(path))

    def remove(self):
        """Removes theme files."""
        for directory in [self.src_dir, self.dst_dir]:
            try:
                shutil.rmtree(directory)
                print("removed", directory)
            except FileNotFoundError:
                pass

    def read_files(self):
        """Reads files from disk (from self.src) into File Objects."""
        if not self.is_unpacked:
            return

        listdir = os.listdir(self.src_dir)
        for file in listdir:
            abs_src = os.path.join(self.src_dir, file)
            abs_dst = os.path.join(self.dst_dir, file)
            name, ext = os.path.splitext(file)

            if os.path.isdir(abs_src):
                shutil.copytree(abs_src, abs_dst)
                self.dirs.append(abs_dst)
            elif ext not in ['.html', '.htm', '.php']:
                shutil.copyfile(abs_src, abs_dst)
                self.dst_files.append(SimpleThemeFile(abs_src, abs_dst))
            else:
                key = os.path.basename(abs_src)
                self.src_files[key] = ParsedThemeFile(abs_src, abs_dst)

    def write_files(self):
        """Writes File Objects to files in self.dst dir."""
        if not self.is_unpacked:
            return

        for file in self.dst_files:
            if file.ready:
                file.write()

        self.is_written = True

    def get_file(self, filename):
        file = self.src_files.get(filename, None)

        if file is not None:
            file.read()

        return file

    def add_file(self, wpath, content):
        file = NewThemeFile(wpath)
        file.content = content
        self.dst_files.append(file)


if __name__ == "__main__":
    src = r"E:\git-workspace\diplom\tmp\snowboarding"
    dst = r"E:\git-workspace\diplom\tmp\uploads\snowboarding"
    request_data = {
        'name': 'test',
        'file': 'test',
        'form': 'Joomla',
        'version': 362,
        'language': 'en-GB',
        'creationDate': '',
        'author': '',
        'authorEmail': '',
        'copyright': '',
        'license': '',
        'authorUrl': '',
    }
    # getter = Getter("Joomla", 362)
    # theme = Theme(src, dst, request_data, getter)
    # theme.remove()
