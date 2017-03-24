# coding: utf-8

from bs4 import BeautifulSoup as bs

from adaptation import settings as adapt_settings
from adaptation.core.adapters import BaseAdapter
from adaptation.core import functions
from adaptation.core.XMLFile import XMLFile


class JoomlaAdapter(BaseAdapter):
    """Class keeps methods for all Joomla adapters"""
    def __init__(self, getter, process_files, data):
        super(JoomlaAdapter, self).__init__(getter, process_files, data)
        self.xml_file = None

    def adapt(self):
        super(JoomlaAdapter, self).adapt()
        self.xml_file = self.build_xml()

    def build_xml(self):
        """
        Realizes building xml file using settings. Returns XMLFile object.

        :return: XMLFile object
        """
        xml_settings = self.settings["XML_DESCRIPTION"]
        xml_file = XMLFile(xml_settings["base"]["name"], xml_settings["base"]["attributes"])

        for xml_tag, text in self.request_data.items():
            if xml_tag not in xml_settings["form_data"]["excluded"]:
                xml_file.add_child(".", xml_tag, text)

        for xml_tag, xml_content in xml_settings["tags"].items():
            if bool(xml_content) is False:
                xml_content = {}
            xml_file.add_child(".", xml_tag, **xml_content)

        for file, file_type in self.uploaded_files["moved"].items():
            xml_file.add_child("files", file_type, file)

        for file in adapt_settings.JOOMLA['FILES']:
            if file.startswith('language'):
                text = file.replace("language", "")
                attributes = {"tag": self.request_data["language"]}
                xml_file.add_child("languages", "language", text, attributes)

        return xml_file

    @staticmethod
    def preparation(content, **kwargs):
        def build_styles(link_tags, settings):
            """
            Builds head_styles for joomla.

            :param link_tags: list of link tags
            :param settings:
            :return: dict <"key": "content">
            """
            page_content = ""
            for link_tag in link_tags:
                if link_tag.attrs["rel"][0] == settings["has_rel"]:
                    href = link_tag.attrs["href"]
                    if not functions.is_url(href):
                        page_content += settings["template"].format(stylesheet=href) + "\n"

            return {
                settings["format_name"]: page_content
            }

        result = {
            "format_update": {},
            "updated_content": "",
        }

        elements = kwargs["elements"]
        preparation_settings = kwargs["settings"]

        styles = build_styles(elements["link"], preparation_settings["STYLES"])
        result["format_update"].update(styles)

        soup = bs(content, "html.parser")
        
        for attachment in preparation_settings["TAGS_ATTACHMENT"]:
            attribute = attachment["attribute"]

            for tag in attachment["tags"]:
                current_tags_list = soup.select(tag)
                
                for current_tag in current_tags_list:
                    old_path = current_tag.attrs.get(attribute, False)
                    
                    if old_path and not functions.is_url(old_path):
                        current_tag.attrs[attribute] = attachment["template"].format(old_path=old_path)

        result["updated_content"] = str(soup)
        return result
