# coding: utf-8
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup as bs

from adaptation.core.BaseAdapter import BaseAdapter


class JoomlaAdapter(BaseAdapter):
    """Base Joomla"""
    def __create_xml__(self):
        extension = ET.Element('extension')
        extension.set('version', '2.5')
        extension.set('type', 'template')
        extension.set('client', 'site')

        # TODO: pretty print xml to file
        for element, value in self.data.items():
            sub_element = ET.SubElement(extension, element)
            sub_element.text = value

        xml_content = ET.tostring(extension, encoding='utf-8', method='xml').decode('utf-8')
        return bs(xml_content, "xml").prettify()





