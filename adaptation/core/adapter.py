# coding: utf-8
import json
import os

import shutil
from django.conf import settings
from adaptation import settings as adapt_settings
from adaptation.core.classes import UserFileNotFoundError, DescriptionKeyNotFoundError

from adaptation.core.functions import split_path


# TODO: test the class
class Adapter:
    def __init__(self, data):
        self.data = data
        self.file = data['file']
        folder, filename, ext = split_path(self.file)

        self.dirs = {
            'src': os.path.join(settings.TEMP_DIR, filename),
            'dst': os.path.join(settings.MEDIA_ROOT, data['name']),
        }

        for directory in self.dirs.values():
            if os.path.exists(directory):
                shutil.rmtree(directory)
            os.mkdir(directory)

    def __del__(self):
        for directory in self.dirs.values():
            if os.path.exists(directory):
                print('Removing %s' % directory)
                shutil.rmtree(directory)

    def adapt(self):
        shutil.unpack_archive(self.file, self.dirs['src'], 'zip')

        description = self.__check_requirements__()
        self.__make_files__(description)

        archived_abs_path = shutil.make_archive(self.dirs['dst'], 'zip',
                                                root_dir=settings.MEDIA_ROOT,
                                                base_dir=self.data['name'])

        return os.path.join(settings.MEDIA_URL, os.path.basename(archived_abs_path))

    def __make_files__(self, description):
        files = self.__get_files__(description)

        for filename, content in files.items():
            path = os.path.join(self.dirs['dst'], filename)

            with open(path, 'w+', encoding='utf-8') as file:
                file.write(content)

    def __check_requirements__(self):
        src = self.dirs['src']

        for required in adapt_settings.COMMON_REQUIRES_FILES:
            absolute_path = os.path.join(src, required)
            if not os.path.exists(absolute_path):
                raise UserFileNotFoundError(required)

        # all required files was found
        description_path = os.path.join(src, adapt_settings.DESCRIPTION_FILE)
        with open(description_path, 'r', encoding='utf-8') as description_file:
            description = json.loads(description_file.read())

        internal_description = {}

        for key in adapt_settings.REQUIRED_DESCRIPTION_KEYS:
            if key in description:
                internal_description[key] = os.path.join(src, description[key])
            else:
                raise DescriptionKeyNotFoundError(key)

        return internal_description

    def __get_files__(self, description):
        return {
            "index.html": "<h1>HelloWorld</h1>",
            "page.html": "<h2>Page</h2>",
        }