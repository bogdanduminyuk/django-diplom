# coding: utf-8
import os
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

from adaptation import settings as adapt_settings
from adaptation.core.BaseAdapter import BaseAdapter
from core import functions


class JoomlaAdapter(BaseAdapter):
    """Class keeps methods for all Joomla adapters"""
    def __init__(self, process_files, data):
        super(JoomlaAdapter, self).__init__(process_files, data)
        self.xml_element = self.__create_base_xml__()
        self.__preparation__()

    def __create_base_xml__(self):
        """
        Creates base structure of templateDetail.xml.

        :return: element of ElementTree
        """
        extension = ET.Element('extension')
        extension.set('version', '2.5')
        extension.set('type', 'template')
        extension.set('client', 'site')

        for element, value in self.data.items():
            if element not in ["form", "file"] + list(adapt_settings.PAGE_PARTS.keys()):
                sub_element = ET.SubElement(extension, element)
                sub_element.text = str(value)

        description = ET.SubElement(extension, 'description')
        description.text = "TPL_WHITESQUARE_XML_DESCRIPTION"

        files = ET.SubElement(extension, 'files')
        positions = ET.SubElement(extension, 'positions')

        languages = ET.SubElement(extension, 'languages')
        languages.set('folder', 'language')

        for file in adapt_settings.JOOMLA['FILES']:
            if file.startswith('language'):
                language = ET.SubElement(languages, 'language')
                language.set('tag', self.data['language'])
                language.text = os.path.basename(file)

        for file, file_type in self.theme_files["moved"].items():
            current_file = ET.SubElement(files, file_type)
            current_file.text = file

        return extension

    @staticmethod
    def __get_pretty_xml__(element):
        """
        Returns pretty xml of given element.

        :param element: ET.Element
        :return: pretty xml string
        """
        rough_string = ET.tostring(element, encoding='utf-8', method='xml')
        re_parsed = minidom.parseString(rough_string)
        return re_parsed.toprettyxml(indent=4*' ', encoding='utf-8').decode('utf-8')

    def __append_files__(self, files):
        xml_files = self.xml_element.find('files')

        for file in files:
            if os.path.basename(file) == file:
                file_element = ET.SubElement(xml_files, 'filename')
                file_element.text = file

    def __preparation__(self):
        def build_styles(link_tags, settings):
            content = ""
            for link_tag in link_tags:
                if link_tag.attrs["rel"][0] == settings["has_rel"]:
                    href = link_tag.attrs["href"]
                    if not functions.is_url(href):
                        content += settings["template"].format(stylesheet=href) + "\n"

            return {
                settings["format_name"]: content
            }

        preparation = self.settings["PREPARATION"]
        styles = build_styles(self.page_elements["link"], preparation["STYLES"])
        self.data.update(styles)
        # print(styles)



