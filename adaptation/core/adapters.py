# coding: utf-8
from bs4 import BeautifulSoup as bs

from adaptation.core.UploadManager import UploadManager
from adaptation.core.getters import Getter
from adaptation.core import functions


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

        for file, content in files.items():
            _content = content.replace('&lt;', '<')
            _content = _content.replace('&gt;', '>')
            files[file] = _content

        return self.upload_manager.download(files)


class BaseAdapter:
    """
    The BaseAdapter class is used for realizing common actions of all adapters.

    It is a base module for all adapter modules.
    """
    def __init__(self, getter, uploaded_files, request_data):
        self.getter = getter
        self.request_data = request_data
        self.format_data = self.request_data.copy()

        self.uploaded_files = uploaded_files
        self.prepared_files = {}

        self.static_path = None
        self.templates = None
        self.settings = None

    def adapt(self):
        self.static_path = self.getter.get_static_root()
        self.templates = self.getter.get_templates()
        self.settings = self.getter.get_settings(self.request_data)

        # Todo: oops! static code...
        filename = self.uploaded_files['other']['index.html']['src']

        prepared = self.getter.get_file_content(filename, self.preparation, self.settings["PREPARATION"])
        prepared_page_parts = self.getter.get_page_parts(prepared["content"])

        self.prepared_files["index"] = {
            "content": prepared["content"],
            "page_parts": prepared_page_parts
        }

        self.update_format_data(prepared["format_update"], prepared_page_parts)

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
            "format_update": {},
            "content": str(soup),
        }

    def update_format_data(self, *args):
        """Updates self.format data using list of args"""
        for arg in args:
            self.format_data.update(arg)
