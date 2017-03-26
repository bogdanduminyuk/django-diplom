# coding: utf-8
import os
import shutil

# TODO: remove after testing
os.environ['DJANGO_SETTINGS_MODULE'] = 'diplom.settings'
from adaptation.core.getters import Getter


class Theme:
    def __init__(self, src, dst, request_data, getter):
        self.src = src
        self.dst = dst
        self.request_data = request_data
        self.settings = getter.get_settings(request_data)
        self.templates = getter.get_templates()
        self.name = request_data["name"]

        self.files = None

        for directory in [self.src, self.dst]:
            if os.path.exists(directory):
                shutil.rmtree(directory)
            os.mkdir(directory)

    def read_files(self):
        """Reads files from disk (from self.src) into File Objects."""
        pass

    def write_files(self):
        """Writes File Objects to files in self.dst dir."""
        pass

    def remove(self):
        """Removes theme files."""
        for directory in [self.src, self.dst]:
            try:
                shutil.rmtree(directory)
                print("removed", directory)
            except FileNotFoundError:
                pass

    def pack(self):
        pass

    def get_file(self, filename):
        return self.files[filename]

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
    getter = Getter("Joomla", 362)
    theme = Theme(src, dst, request_data, getter)
    theme.remove()
