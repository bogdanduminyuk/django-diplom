# coding: utf-8
import os

from adaptation import settings as adapt_settings
from adaptation.core import functions
from adaptation.core.theme import XMLFile
from adaptation.core.adapters import BaseAdapter


class JoomlaAdapter(BaseAdapter):
    """Class keeps methods for all Joomla adapters"""
    def __init__(self, theme, settings, templates, request_data):
        super(JoomlaAdapter, self).__init__(theme, settings, templates, request_data)
        self.xml_file = None

    def adapt(self, **kwargs):
        super(JoomlaAdapter, self).adapt(**kwargs)
        self.xml_file = self.build_xml()

    def build_xml(self):
        """
        Realizes building xml file using settings. Returns XMLFile object.

        :return: XMLFile object
        """
        xml_settings = self.settings["XML_DESCRIPTION"]
        xml_file = XMLFile(rpath="",
                           wpath=os.path.join(self.theme.dst_dir, xml_settings["path"]),
                           main_element_name=xml_settings["base"]["name"],
                           attributes=xml_settings["base"]["attributes"])

        for xml_tag, text in self.request_data.items():
            if xml_tag not in xml_settings["form_data"]["excluded"]:
                xml_file.add_child(".", xml_tag, text)

        for xml_tag, xml_content in xml_settings["tags"].items():
            if bool(xml_content) is False:
                xml_content = {}
            xml_file.add_child(".", xml_tag, **xml_content)

        # for file, file_type in self.uploaded_files["moved"].items():
        #    xml_file.add_child("files", file_type, file)

        for file in adapt_settings.JOOMLA['FILES']:
            if file.startswith('language'):
                text = file.replace("language", "")
                attributes = {"tag": self.request_data["language"]}
                xml_file.add_child("languages", "language", text, attributes)

        for directory in self.theme.directories:
            xml_file.add_child("files", "folder", directory.basename)
        for file in self.theme.dst_files:
            xml_file.add_child("files", "filename", file.basename)

        return xml_file

    @staticmethod
    def prepare(file, **kwargs):
        super(JoomlaAdapter, JoomlaAdapter).prepare(file, **kwargs)

        joomla_styles_settings = kwargs["settings"]["STYLES"]
        styles = ""
        elements = file.get_page_elements()
        for link_tag in elements["link"]:
            if link_tag.attrs["rel"][0] == joomla_styles_settings["has_rel"]:
                href = link_tag.attrs["href"]
                if not functions.is_url(href):
                    styles += joomla_styles_settings["template"].format(stylesheet=href) + "\n"

        kwargs["templates_data"].update({
            joomla_styles_settings["format_name"]: styles
        })
