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
        self.getter = Getter(self.request_data['form'], self.request_data['version'])

    def adapt(self):
        current_adapter = self.getter.get_adapter()
        uploaded_files = self.upload_manager.upload()

        files = current_adapter(uploaded_files, self.request_data).adapt()

        return self.upload_manager.download(files)


class BaseAdapter:
    """
    The BaseAdapter class is used for realizing common actions of all adapters.

    It is a base module for all adapter modules.
    """
    def __init__(self, getter, uploaded_files, request_data):
        self.getter = getter
        self.uploaded_files = uploaded_files
        self.request_data = request_data

        self.static_path = None
        self.templates = None
        self.settings = None

        self.format_data = {}

    def adapt(self):
        self.static_path = self.getter.get_static_path()
        self.templates = self.getter.get_templates()
        self.settings = self.getter.get_settings()
