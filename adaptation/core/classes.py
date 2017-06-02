# coding: utf-8
import json
import os

from adaptation import settings as adapt_settings
from adaptation.core.file_types import TemplateFile
from diplom import settings


class Getter:
    def __init__(self, adaptation_type, cms_version):
        self.adapt_type = adaptation_type
        self.version = cms_version

    def get_plugin(self, adapt_type="", version=""):
        """Returns class of current adapter."""
        adapt_type = adapt_type if adapt_type else self.adapt_type
        version = version if version else self.version

        if not version:
            exec("import adaptation.plugins.{type}.p{version} as plugin".format(type=adapt_type,
                                                                                version=version))
            PluginClass = eval("plugin.Plugin")
        else:
            exec("import adaptation.plugins.{type} as plugin".format(type=adapt_type))
            PluginClass = eval("plugin.Base{type}Plugin".format(type=adapt_type))

        return PluginClass

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

    @staticmethod
    def get_user_cfg():
        """Returns dict of user settings from user.json."""
        with open(settings.USER_CONFIG, 'r', encoding='utf-8') as cfg:
            return json.loads(cfg.read())
