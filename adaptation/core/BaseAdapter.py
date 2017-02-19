# coding: utf-8
import os

from adaptation import settings as adapt_settings


class BaseAdapter:
    """The BaseAdapter class is used for realizing common actions of all adapters."""
    def __init__(self, files_to_work, data):
        self.data = self.__create_full_data__(files_to_work, data)

    def __create_full_data__(self, files_to_work, data):
        adapt_type = data['form'].upper()
        static_cms_root = adapt_settings.STATIC_CMS_ROOT.format(form=data['form'])
        cms_settings = eval("adapt_settings.{}".format(adapt_type))
        templates = self.__get_templates__(static_cms_root)

        # exec format with FILES-keys
        for key in cms_settings['FILES']:
            cms_settings['FILES'][key.format(**data)] = cms_settings["FILES"].pop(key)

        return {
            "DATA": data,
            "SETTINGS": cms_settings,
            "TEMPLATES": templates,
            "PROCESS_FILES": files_to_work,
        }

    @staticmethod
    def __get_templates__(static_cms_root):
        templates_dict = {}
        templates_path = os.path.join(static_cms_root, 'tpl')

        for template in os.listdir(templates_path):
            abs_path = os.path.join(templates_path, template)
            with open(abs_path, 'r', encoding='utf-8') as template_file:
                templates_dict[template] = {
                    "content": template_file.read(),
                    "path": abs_path
                }

        return templates_dict
