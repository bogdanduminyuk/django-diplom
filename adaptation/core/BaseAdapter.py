# coding: utf-8
from adaptation import settings as adapt_settings


class BaseAdapter:
    """The BaseAdapter class is used for realizing common actions of all adapters."""
    def __init__(self, theme_files, request_data):
        adapt_type = request_data['form'].upper()
        static_cms_root = adapt_settings.STATIC_CMS_ROOT.format(form=request_data['form'])

        # clear data is used in building xml file in joomla adapter
        self.clear_data = request_data.copy()

        # all data for filling format
        self.data = request_data

        self.theme_files = theme_files
        self.templates = self.__get_templates__(static_cms_root)
        self.settings = self.__get_settings__(adapt_type, request_data)
        self.index_content = self.__get_index_content__(theme_files["other"])

        self.__custom_preparation__()
        self.data.update(self.__get_page_parts__(self.index_content))

    def __custom_preparation__(self):
        """it is here for redeclaration in children."""
        pass
