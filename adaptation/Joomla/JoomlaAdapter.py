# coding: utf-8
import os

from adaptation import settings as adapt_settings
from adaptation.core import functions
from adaptation.core.theme import XMLFile
from adaptation.core.adapters import BaseAdapter


class JoomlaAdapter(BaseAdapter):
    """Class keeps methods for all Joomla adapters"""
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

        for file in adapt_settings.JOOMLA['FILES']:
            if file.startswith('language'):
                text = file.replace("language", "")
                attributes = {"tag": self.request_data["language"]}
                xml_file.add_child("languages", "language", text, attributes)

        for directory in self.theme.directories:
            xml_file.add_child("files", "folder", directory.basename)

        for file in self.theme.get_root_files():
            xml_file.add_child("files", "filename", file.basename)

        return xml_file

    @staticmethod
    def prepare(file, **kwargs):
        """
        Realizes Joomla preparation.

        :param file: ParsableThemeFile to prepare
        :param kwargs: dict of additional arguments
        :return: None
        """
        def get_additional(collection, attribute, template):
            """
            Realizes creation of addStylesheet or addScript.

            :param collection: list of tags
            :param attribute: tag attribute where it search for value
            :param template: string that used as format template
            :return: string
            """
            joomla_add_string = ""

            for tag in collection:
                attr_value = tag.attrs.get(attribute, "")
                if attr_value and not functions.is_url(attr_value):
                    joomla_add_string += template.format(attr_value) + "\n"

            return joomla_add_string

        super(JoomlaAdapter, JoomlaAdapter).prepare(file, **kwargs)

        styles_template = kwargs["settings"]["STYLES"]["template"]
        scripts_template = kwargs["settings"]["SCRIPTS"]["template"]

        styles = get_additional(file.get_page_elements()['link'], 'href', styles_template)
        scripts = get_additional(file.soup.select("head script"), 'src', scripts_template)

        kwargs["template_data"].update({
            kwargs["settings"]["STYLES"]["format_name"]: styles,
            kwargs["settings"]["SCRIPTS"]["format_name"]: scripts
        })
