# coding: utf-8
from bs4 import BeautifulSoup as bs

from adaptation.core import functions
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
            self.adapter(self.uploader.theme, self.settings, self.templates, self.request_data).adapt()
            return self.uploader.download()
        finally:
            self.uploader.theme.remove()


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
        self.template_data = request_data.copy()

    def adapt(self, **kwargs):
        index_file = self.theme.get_file("index.html")
        self.prepare(index_file,
                     settings=self.settings["PREPARATION"],
                     template_data=self.template_data)

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

        file.set_content(str(soup))
        kwargs["template_data"].update(file.get_page_parts())
