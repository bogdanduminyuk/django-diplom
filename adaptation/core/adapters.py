# coding: utf-8
from adaptation.core.classes import Getter, Uploader


class Adapter:
    """
    Class is used as interface for adaptation.

    Just call adapt-method for make adaptation.
    """
    def __init__(self, request_data):
        getter = Getter(request_data["form"], request_data["version"])

        self.request_data = request_data
        self.uploader = Uploader()
        self.settings = getter.get_settings(request_data)
        self.templates = getter.get_templates()
        self.adapter = getter.get_adapter()

    def adapt(self):
        self.uploader.upload(self.request_data["file"], self.request_data["name"])
        self.uploader.theme.read_files()
        try:
            self.adapter(self.uploader.theme).adapt(self.settings, self.templates)
        finally:
            self.uploader.theme.remove()
        return self.uploader.download()


class BaseAdapter:
    """
    The BaseAdapter class is used for realizing common actions of all adapters.

    It is a base module for all adapter modules.
    """
    def __init__(self, theme):
        self.theme = theme

    def adapt(self, settings, templates, **kwargs):
        pass
