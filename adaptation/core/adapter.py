# coding: utf-8
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
        theme_files = self.upload_manager.upload()

        files = current_adapter(theme_files, self.request_data).adapt()

        return self.upload_manager.download(files)
