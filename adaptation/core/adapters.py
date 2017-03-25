# coding: utf-8
from bs4 import BeautifulSoup as bs

from adaptation.core.UploadManager import UploadManager
from adaptation.core.getters import Getter
from core import functions


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

        files = current_adapter(self.getter, uploaded_files, self.request_data).adapt()

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

        self.format_data = self.request_data.copy()

    def adapt(self):
        self.static_path = self.getter.get_static_path()
        self.templates = self.getter.get_templates()
        self.settings = self.getter.get_settings(self.request_data)

        filename = self.uploaded_files['other']['index.html']['src']
        preparation_result = self.getter.get_file_content(filename, self.preparation, self.settings["PREPARATION"])
        self.format_data.update(preparation_result["format_update"])

    @staticmethod
    def preparation(content, **kwargs):
        """
        Realizes replacing in settings[tags_attachment]

        :param content: page content
        :param kwargs: dict of settings and necessary data
        :return: dict with one key "updated_content"
        """
        soup = bs(content, "html.parser")

        for attachment in kwargs["settings"]["TAGS_ATTACHMENT"]:
            attribute = attachment["attribute"]

            for tag in attachment["tags"]:
                current_tags_list = soup.select(tag)

                for current_tag in current_tags_list:
                    old_path = current_tag.attrs.get(attribute, False)

                    if old_path and not functions.is_url(old_path):
                        current_tag.attrs[attribute] = attachment["template"].format(old_path=old_path)

        return {
            "updated_content": str(soup)
        }
