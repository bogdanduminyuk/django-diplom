# coding: utf-8
from adaptation import settings as adapt_settings
from adaptation.core.UploadManager import UploadManager
from adaptation.core.getters import Getter


class Adapter:
    """
    Class is used as interface for adaptation.

    Just call adapt-method for make adaptation.
    """
    def __init__(self, request_data):
        self.request_data = request_data
        self.upload_manager = UploadManager(request_data['file'], request_data['name'])

    def adapt(self):
        getter = Getter(self.request_data['form'], self.request_data['version'])
        current_adapter = getter.get_adapter()
        uploaded_files = self.upload_manager.upload()

        files = current_adapter(uploaded_files, self.request_data).adapt()

        return self.upload_manager.download(files)


class BaseAdapter:
    """The BaseAdapter class is used for realizing common actions of all adapters."""
    def __init__(self, uploaded_files, request_data):
        adapt_type = request_data['form'].upper()
        static_cms_root = adapt_settings.STATIC_CMS_ROOT.format(form=request_data['form'])

        # clear data is used in building xml file in joomla adapter
        self.clear_data = request_data.copy()

        # all data for filling format
        self.data = request_data

        self.uploaded_files = uploaded_files
        self.templates = self.__get_templates__(static_cms_root)
        self.settings = self.__get_settings__(adapt_type, request_data)
        self.index_content = self.__get_index_content__(uploaded_files["other"])

        self.__custom_preparation__()
        self.data.update(self.__get_page_parts__(self.index_content))

    def __custom_preparation__(self):
        """it is here for redeclaration in children."""
        pass
