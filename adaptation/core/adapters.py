# coding: utf-8
from bs4 import BeautifulSoup as bs

from adaptation.core.classes import Getter, Uploader
from adaptation.core import functions


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
            self.adapter(self.uploader.theme, self.settings, self.templates, self.request_data).adapt()
        finally:
            self.uploader.theme.remove()
        return self.uploader.download()


class BaseAdapter:
    """
    The BaseAdapter class is used for realizing common actions of all adapters.

    It is a base module for all adapter modules.
    """
    def __init__(self, theme, settings, templates, request_data):
        self.theme = theme
        self.settings = settings
        self.templates = templates
        self.request_data = request_data

    def adapt(self, **kwargs):
        index_file = self.theme.get_file("index.html")
        # index_file.read()
        index_file.prepare(self.preparation, self.settings["PREPARATION"])

    @staticmethod
    def prepare(file, **kwargs):
        """
        Realizes replacing in settings[tags_attachment]

        :param file: ParsedThemeFile
        :param kwargs: additional args
        :return: None
        """
        soup = bs(file.get_content(), "html.parser")
        for attachment in kwargs["settings"]["TAGS_ATTACHMENT"]:
            attribute = attachment["attribute"]

            for tag in attachment["tags"]:
                current_tags_list = soup.select(tag)

                for current_tag in current_tags_list:
                    old_path = current_tag.attrs.get(attribute, False)

                    if old_path and not functions.is_url(old_path):
                        current_tag.attrs[attribute] = attachment["template"].format(old_path=old_path)

        # todo: None return File is modified by ref
        return {
            "format_update": {},
            "content": str(soup),
        }

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
