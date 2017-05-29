# coding: utf-8
import os

from bs4 import BeautifulSoup as bs

from adaptation.core import functions
from adaptation.core.classes import Getter, Uploader
from base import settings as base_settings


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

        if not self.uploader.theme.src_parsable_files:
            raise Exception("Ошибка инициализации темы. Не найдены файлы для парсинга.")

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
        for attachment in kwargs["settings"]["TAGS_ATTACHMENT"]:
            tags_dict = file.get_page_tags(*attachment["tags"], parent=attachment.get("parent", ""))

            for description in tags_dict.values():
                attribute = description["info"]["attribute"]

                for tag_element in description["selection"]:
                    old_path = tag_element.attrs.get(attribute, False)
                    if old_path and not functions.is_url(old_path):
                        tag_element.attrs[attribute] = attachment["template"].format(old_path=old_path)

        kwargs["template_data"].update({
            page_part: selection[0]
            for page_part, selection in file.get_page_parts().items()
        })

    def get_template(self, filename):
        """Returns template for given filename if it exists or None otherwise."""
        template_name = os.path.basename(filename) + ".tpl"

        if template_name in self.templates.keys():
            return self.templates[template_name]
