# coding: utf-8
import os

from bs4 import BeautifulSoup as bs

from adaptation import settings as adapt_settings


class BaseAdapter:
    """The BaseAdapter class is used for realizing common actions of all adapters."""
    def __init__(self, theme_files, data):
        adapt_type = data['form'].upper()
        static_cms_root = adapt_settings.STATIC_CMS_ROOT.format(form=data['form'])

        self.data = data
        self.theme_files = theme_files
        self.templates = self.__get_templates__(static_cms_root)
        self.settings = self.__get_settings__(adapt_type, data)
        self.index_content = self.__get_index_content__(theme_files["other"])

        # self.__custom_preparation__()

        self.data.update(self.__get_page_parts__(self.index_content))
        self.page_elements = self.__get_page_elements__(self.index_content)

    def __custom_preparation__(self):
        """it is here for redeclaration in children."""
        pass

    @staticmethod
    def __get_settings__(adapt_type, data):
        """
        Gets current settings for current CMS type.

        :param adapt_type: current adapt type eg WordPress, Joomla.
        :param data: data that came from form
        :return: settings dict
        """
        settings = eval("adapt_settings.{}".format(adapt_type))

        # exec format with FILES-keys
        for key in settings['FILES']:
            settings['FILES'][key.format(**data)] = settings["FILES"].pop(key)

        return settings

    @staticmethod
    def __get_templates__(static_cms_root):
        """
        Returns current templates dictionary.

        :param static_cms_root: directory of static template files.
        :return: dict of templates <filename : content>
        """
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

    @staticmethod
    def __get_page_parts__(index_content):
        """
        Realizes selection using selectors.

        :param index_content: content where it looks for.
        :return: dict <page_part : content>
        """
        parts = {}
        soup = bs(index_content, 'html.parser')

        for part, values in adapt_settings.PAGE_PARTS.items():
            selector = values["SELECTOR"]
            parts[part] = str(soup.select(selector)[0])

        return parts

    @staticmethod
    def __get_index_content__(process_files):
        """
        Returns content of index file.

        :param process_files: dict of files to process
        :return: string of index content
        """
        for filename, data in process_files.items():
            if filename.startswith('index'):
                with open(data['src'], 'r', encoding='utf-8') as file:
                    return file.read()

        return None

    @staticmethod
    # TODO: it is not used
    def __get_page_elements__(index_content):
        """
        Returns a dict of lists those contain tags.

        Tags are described in adapt_settings.PAGE_ELEMENTS.
        :param index_content: page content where find tags
        :return: dict of tags lists
        """
        soup = bs(index_content, "html.parser")
        elements = {}

        for page_element in adapt_settings.PAGE_ELEMENTS:
            elements_list = soup.select(page_element)
            elements[page_element] = elements_list

        return elements


