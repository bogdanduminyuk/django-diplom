# coding: utf-8

import os
import shutil

from adaptation import settings as adapt_settings
from adaptation.core.theme import TemplateFile, Theme
from diplom import settings


class Uploader:
    def __init__(self):
        self.theme = None

    def upload(self, src_zip, theme_name):
        """
        Creates theme.

        :param src_zip: uploaded zip archive
        :param theme_name: theme name from request data
        :return: Theme object
        """
        src_dir = os.path.join(settings.TEMP_DIR, os.path.splitext(os.path.basename(src_zip))[0])
        dst_dir = os.path.join(settings.MEDIA_ROOT, theme_name)

        self.make_dirs(src_dir, dst_dir)

        self.theme = Theme(src_zip, src_dir, dst_dir, theme_name)
        self.theme.unpack()
        return self.theme

    def download(self):
        """Returns link to packed theme."""
        return self.theme.pack()

    @staticmethod
    def make_dirs(*directories):
        for directory in directories:
            if os.path.exists(directory):
                shutil.rmtree(directory)
            os.mkdir(directory)


class Getter:
    def __init__(self, adaptation_type, cms_version):
        self.adapt_type = adaptation_type
        self.version = cms_version

    def get_adapter(self, adapt_type="", version=""):
        """Returns class of current adapter."""
        adapt_type = adapt_type if adapt_type else self.adapt_type
        version = version if version else self.version

        adapter_class = adapt_type + "Adapter" + str(version)
        exec("import adaptation.{package}.{adapter_class} as adapter".format(package=adapt_type,
                                                                             adapter_class=adapter_class))
        obj = eval("adapter.{adapter_class}".format(adapter_class=adapter_class))
        return obj

    def get_settings(self, request_data):
        """Returns current settings dict."""
        cms_settings = eval("adapt_settings.{}".format(self.adapt_type.upper()))

        # exec format with FILES-keys
        for key in cms_settings['FILES']:
            cms_settings['FILES'][key.format(**request_data)] = cms_settings["FILES"].pop(key)

        return cms_settings

    def get_static_root(self):
        """Returns path to CMS static files."""
        return adapt_settings.STATIC_CMS_ROOT.format(package=self.adapt_type)

    def get_templates_root(self):
        """Returns path to CMS templates files."""
        return adapt_settings.TEMPLATES_ROOT.format(package=self.adapt_type)

    def get_templates(self):
        """Returns current templates dictionary."""
        templates_dict = {}
        templates_path = self.get_templates_root()

        for template in os.listdir(templates_path):
            abs_path = os.path.join(templates_path, template)
            templates_dict[template] = TemplateFile(abs_path)

        return templates_dict
