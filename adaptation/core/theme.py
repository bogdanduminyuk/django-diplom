# coding: utf-8
import os
import shutil
import xml.dom.minidom as minidom
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup as bs

from adaptation import settings as adapt_settings
from diplom import settings
from base import settings as base_settings


class FileSystemObject:
    """Class is base for objects of file system (files, directories)."""
    def __init__(self, rpath, wpath):
        self.rpath = rpath
        self.wpath = wpath
        self.basename = os.path.basename(rpath) if rpath else os.path.basename(wpath)

    def copy(self):
        pass


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
        self.dirname = os.path.dirname(wpath)

    def read(self):
        """Simple file reading."""
        if self.rpath:
            with open(self.rpath, "r", encoding="utf-8") as file:
                self.content = file.read()
                return self.content

    def write(self):
        """Simple file writing."""
        if self.wpath:
            if not os.path.exists(self.dirname):
                os.makedirs(self.dirname)

            with open(self.wpath, "w", encoding="utf-8") as file:
                file.write(self.content)

    def get_content(self, **kwargs):
        return self.content

    def copy(self):
        """Copies file from rpath to wpath"""
        shutil.copyfile(self.rpath, self.wpath)


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


class ParsableThemeFile(FileObject):
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
        self.prepared = True

    def get_selection(self, selector, as_string=False):
        """Realizes simple selection by selector."""
        selection = self.soup.select(selector)
        return [str(i).replace('&lt;', '<').replace('&gt;', '>') for i in selection] if as_string else selection

    def get_page_parts(self, *parts, as_string=True):
        """
        Returns dict of <page_part: selection> by given keys.

        If keys is False returns  the same dict constructed from all page parts.

        :param parts: tuple of string keys
        :param as_string: bool parameter means to return tags as string or BS.tags
        :return: dict
        """
        intersection = set(parts) & adapt_settings.PAGE_PARTS.keys()
        keys = intersection if intersection else adapt_settings.PAGE_PARTS.keys()

        return {
            key: self.get_selection(value["SELECTOR"], as_string)
            for key, value in adapt_settings.PAGE_PARTS.items() if key in keys
        }

    def get_page_tags(self, *tags, parent="", as_string=False):
        """
        Realizes getting tags info and selection.

        If tags does not given then method uses all tags the system knows.

        If parent does not given the selection search globally otherwise it uses 'parent tag_name' selector.

        :param tags: tuple of tags
        :param parent: parent selector e.g. 'body script'
        :param as_string: bool parameter means to return tags as string or BS.tags
        :return: dict <tag_name: <"selection":selection, "info":info> >
        """
        intersection = set(tags) & base_settings.TAGS.keys()
        keys = intersection if intersection else base_settings.TAGS.keys()

        return {
            tag_name: {
                "selection": self.get_selection(parent + " " + tag_name if parent else tag_name, as_string),
                "info": data
            }
            for tag_name, data in base_settings.TAGS.items() if tag_name in keys
        }

    def replace(self, page_part_key, template):
        """
        Realizes soup replacement of page part to template.

        :param page_part_key: key of page part
        :param template: template to replace
        :return: None
        """
        selector = adapt_settings.PAGE_PARTS[page_part_key]["SELECTOR"]
        selection = self.soup.select(selector)[0]
        selection.replace_with(template)


class Theme:
    def __init__(self, src_zip, src_dir, dst_dir, name):
        self.src_zip = src_zip
        self.src_dir = src_dir
        self.dst_dir = dst_dir
        self.name = name
        self.is_unpacked = False
        self.is_written = False

        self.other_files = []
        self.directories = []
        self.dst_files = []
        self.src_parsable_files = {}

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
                self.directories.append(DirectoryObject(abs_src, abs_dst))
            elif ext not in ['.html', '.htm', '.php']:
                self.other_files.append(FileObject(abs_src, abs_dst))
            else:
                file = ParsableThemeFile(abs_src, abs_dst)
                self.src_parsable_files[file.basename] = file

    def write_files(self):
        """Writes File Objects to files in self.dst dir."""
        if not self.is_unpacked:
            return

        for obj in self.directories + self.other_files:
            obj.copy()

        for file in self.dst_files:
            file.write()

        self.is_written = True

    def get_file(self, filename):
        """Returns ParsableFile and read it."""
        file = self.src_parsable_files.get(filename, None)

        if file is not None:
            file.read()

        return file

    def add_file(self, wpath, content):
        """Appends FileObject to dst theme files"""
        wpath = os.path.join(self.dst_dir, wpath)
        file = FileObject("", wpath)
        file.content = content
        self.dst_files.append(file)

    def get_root_files(self):
        """Returns list of files that will be placed in theme root dir."""
        files = self.other_files + self.dst_files
        return [file for file in files if os.path.relpath(self.dst_dir, file.wpath) == ".."]


if __name__ == "__main__":
    pass
