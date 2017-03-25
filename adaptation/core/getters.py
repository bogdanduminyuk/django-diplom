# coding: utf-8
import os

from adaptation import settings as adapt_settings


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
        settings = eval("adapt_settings.{}".format(self.adapt_type.upper()))

        # exec format with FILES-keys
        for key in settings['FILES']:
            settings['FILES'][key.format(**request_data)] = settings["FILES"].pop(key)

        return settings

    def get_static_root(self):
        """Returns path to CMS static files."""
        return adapt_settings.STATIC_CMS_ROOT.format(package=self.adapt_type)

    def get_templates_root(self):
        """Returns path to CMS templates files."""
        return adapt_settings.TEMPLATES_ROOT.format(package=self.adapt_type)

    def get_templates(self):
        """Returns current templates dictionary."""
        # TODO: remake it to return TemplateFile
        templates_dict = {}
        templates_path = self.get_templates_root()

        for template in os.listdir(templates_path):
            abs_path = os.path.join(templates_path, template)
            with open(abs_path, 'r', encoding='utf-8') as template_file:
                templates_dict[template] = {
                    "content": template_file.read(),
                    "path": abs_path
                }

        return templates_dict
