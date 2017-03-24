# coding: utf-8
import os

from bs4 import BeautifulSoup as bs

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

    def get_static_path(self):
        """Returns path to CMS static files."""
        return adapt_settings.STATIC_CMS_ROOT.format(package=self.adapt_type)

    def get_templates(self):
        """Returns current templates dictionary."""
        templates_dict = {}
        templates_path = os.path.join(self.get_static_path(), 'tpl')

        for template in os.listdir(templates_path):
            abs_path = os.path.join(templates_path, template)
            with open(abs_path, 'r', encoding='utf-8') as template_file:
                templates_dict[template] = {
                    "content": template_file.read(),
                    "path": abs_path
                }

        return templates_dict

    @staticmethod
    def get_page_parts(content):
        """
        Realizes selection using selectors.

        :param content: content where it looks for.
        :return: dict <page_part : content>
        """
        parts = {}
        soup = bs(content, 'html.parser')

        for part, values in adapt_settings.PAGE_PARTS.items():
            selector = values["SELECTOR"]
            parts[part] = str(soup.select(selector)[0])

        return parts

    @staticmethod
    def get_file_content(filename, preparation_method, preparation_settings):
        """Returns content of file with given filename using preparation method."""
        with open(filename, "r", encoding="utf-8") as file:
            content = file.read()
            kwargs = {
                "elements": Getter.get_page_elements(content),
                "settings": preparation_settings,
            }

            preparation_result = preparation_method(content, **kwargs)
            page_parts = Getter.get_page_parts(preparation_result["updated_content"])
            preparation_result["format_update"].update(page_parts)
            return preparation_result

    @staticmethod
    def get_page_elements(content):
        """
        Returns a dict of lists those contain tags.

        Tags are described in adapt_settings.PAGE_ELEMENTS.
        :param content: page content where find tags
        :return: dict of tags lists
        """
        soup = bs(content, "html.parser")
        elements = {}

        for page_element in adapt_settings.PAGE_ELEMENTS:
            elements_list = soup.select(page_element)
            elements[page_element] = elements_list

        return elements


