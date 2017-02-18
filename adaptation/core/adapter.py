# coding: utf-8
import json
import os
import distutils.dir_util as dir_util

import shutil
from django.conf import settings
from adaptation import settings as adapt_settings
from adaptation.core.classes import UserFileNotFoundError, DescriptionKeyNotFoundError, AdaptationTypeError

from adaptation.core.functions import split_path


class Adapter:
    """
    Class is used as interface for adaptation.

    Just call adapt-method for make adaptation.
    """
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

    def __create_description__(self, public_data):
        """
        Returns dict of full description with settings and additional info.

        Also executes format of FILES-keys using self.data.

        :param public_data: data got by __check_requirements__
        :return: dict of full system description
        """
        adapt_type = self.data['form'].upper()
        static_cms_root = adapt_settings.STATIC_CMS_ROOT.format(form=self.data['form'])
        cms_settings = eval("adapt_settings.{}".format(adapt_type))
        templates = self.__get_templates__(static_cms_root, cms_settings["FILES"])

        # exec format with FILES-keys
        for key in cms_settings['FILES']:
            cms_settings['FILES'][key.format(**self.data)] = cms_settings["FILES"].pop(key)

        return {
            "PUBLIC": public_data,
            "PRIVATE": {
                "SETTINGS": cms_settings,
                "DIRS": self.dirs,
                "TYPE": adapt_type,
                "TEMPLATES": templates,
            }
        }

    @staticmethod
    def __get_templates__(static_cms_root, files):
        """
        Gets templates for current cms from static folder.

        :param static_cms_root: path to dir of curr cms static files
        :param files: dict of files from settings
        :return: dict { template name : template_content }
        """
        templates_dict = {}
        templates_path = os.path.join(static_cms_root, 'tpl')

        for file, content in files.items():
            if content == "{content}":
                curr_template_name = file + '.tpl'
                curr_template_path = os.path.join(templates_path, curr_template_name)

                if os.path.exists(curr_template_path):
                    with open(curr_template_path, "r", encoding='utf-8') as template_file:
                        template_content = template_file.read()
                        templates_dict[curr_template_name] = {
                            "content": template_content,
                            "path": curr_template_path
                        }

        return templates_dict

    def adapt(self):
        """
        External adapt function. It means path_layer handling.

        It unpacks input zip, checks requirements and creates files.

        :return: href to result archive
        """
        shutil.unpack_archive(self.file, self.dirs['src'], 'zip')

        public_data = self.__check_requirements__()
        description = self.__create_description__(public_data)

        self.__make_files__(description, self.dirs['dst'])

        archived_abs_path = shutil.make_archive(self.dirs['dst'], 'zip',
                                                root_dir=settings.MEDIA_ROOT,
                                                base_dir=self.data['name'])

        return os.path.join(settings.MEDIA_URL, os.path.basename(archived_abs_path))

    def __make_files__(self, description, dst_dir):
        """
        Files handling.

        Gets settings for current adaptation type. Creates tree and writes files.

        Writes dict{filename : content} to files in dst_dir.
        The dict is result of __get_files__.

        :param description: json description from zip
        :return: None
        """
        cms_settings = description["PRIVATE"]["SETTINGS"]

        dir_util.create_tree(dst_dir, cms_settings["FILES"].keys())

        # copying data from src folders to dst folders
        for key in description["PUBLIC"]:
            if key in cms_settings["DIR_NAMES"]:
                src_path = description["PUBLIC"][key]
                dst_path = os.path.join(dst_dir, cms_settings['DIR_NAMES'][key])

                dir_util.copy_tree(src_path, dst_path)

        files = self.__get_files__(description)

        # write all files with format
        for filename, content in files.items():
            abs_path = os.path.join(self.dirs['dst'], filename)
            with open(abs_path, "w", encoding='utf-8') as file:
                file.write(content)

    def __check_requirements__(self):
        """
        Checks if requirements are complied.

        :return: description dict of absolute paths of files in description
        """
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
        """
        Gets files of custom cms.

        :param description: passed to custom cms adapt method
        :return: returns dict of files and content
        """
        if self.data['form'] in adapt_settings.CMS:
            package = self.data['form']
            adapter_shortcut = "adapter"
            adapter_class = '{0}Adapter{1}'.format(self.data['form'], self.data['version'])
            import_string = 'import adaptation.{0}.{1} as {2}'.format(package, adapter_class, adapter_shortcut)
            call_string = '{0}.{1}(description, self.data).adapt()'.format(adapter_shortcut, adapter_class)
        else:
            raise AdaptationTypeError(self.data['form'])

        exec(import_string)
        files = eval(call_string)

        return files


class BaseAdapter:
    """The BaseAdapter class is used for realizing common actions of all adapters."""
    def __init__(self, description, data):
        self.description = description
        self.data = data
