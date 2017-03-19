# coding: utf-8
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom


class XMLFile:
    """Realizes working with xml files. Represents one xml file."""
    def __init__(self, main_element_name, attributes=None):
        self.base_element = ET.Element(main_element_name)
        self.__add_attributes__(self.base_element, attributes)

    def add_child(self, append_to, name, text="", attributes=None):
        """
        Creates and append child to append_to_element
        :param append_to: xpath for element where to append
        :param name: name of new element
        :param text: text of new element
        :param attributes: attributes of new element
        :return: None
        """
        parent = self.base_element.find(append_to)
        sub_element = ET.SubElement(parent, name)
        sub_element.text = str(text)
        self.__add_attributes__(sub_element, attributes)

    def prettify(self):
        """
        Returns pretty xml of self.base_element.

        :return: pretty xml string
        """
        rough_string = ET.tostring(self.base_element, encoding='utf-8', method='xml')
        re_parsed = minidom.parseString(rough_string)
        return re_parsed.toprettyxml(indent=4 * ' ', encoding='utf-8').decode('utf-8')

    @staticmethod
    def __add_attributes__(element, attributes):
        """
        Adds attributes to the element.

        :param element: XML-element
        :param attributes: dict of attributes <attr : value>
        """
        if attributes is not None:
            for attribute, value in attributes.items():
                element.set(attribute, str(value))


if __name__ == "__main__":
    file = XMLFile("extension", {"version": 1.0, "type": "template", "client": "site"})
    appended_children = [
        (".", "files1"),
        (".", "empty_tags"),
        (".", "files3"),
        (".", "sub_tags_with_attributes"),
        ("empty_tags", "sub_empty_tags1", "template_text"),
        ("empty_tags", "sub_empty_tags2", "template_text"),
        ("empty_tags", "sub_empty_tags3", "template_text"),
        ("sub_tags_with_attributes", "sub_tags_with_attributes1", "template_text", {"attr1": 1, "attr2": 2}),
        ("sub_tags_with_attributes", "sub_tags_with_attributes2", "template_text", {"attr1": 1, "attr2": 2}),
    ]

    for params in appended_children:
        file.add_child(*params)

    print(file.prettify())
