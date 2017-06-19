import os

from adaptation.core import functions
from adaptation.plugins import BasePlugin
from adaptation.core.file_types import XMLFile, FileObject


class BaseJoomlaPlugin(BasePlugin):
    def adapt(self):
        def get_additional(collection, template):
            """
            Realizes creation of addStylesheet or addScript.

            :param collection: list of tags
            :param attribute: tag attribute where it search for value
            :param template: string that used as format template
            :return: string
            """
            joomla_add_string = ""
            attribute = collection['info']['attribute']

            for tag in collection["selection"]:
                attr_value = tag.attrs.get(attribute, "")
                if attr_value and not functions.is_url(attr_value):
                    joomla_add_string += template.format(attr_value) + "\n"

            return joomla_add_string

        replacement = []

        index = self.uploaded_theme.get_file('index.html')

        # fill replacement
        for attachment in self.settings["PREPARATION"]["TAGS_ATTACHMENT"]:
            tags_dict = index.get_page_tags(*attachment["tags"], parent=attachment.get("parent", ""))

            for description in tags_dict.values():
                attribute = description["info"]["attribute"]

                for tag_element in description["selection"]:
                    old = tag_element.attrs.get(attribute, False)

                    if old and not functions.is_url(old):
                        replacement.append({
                            "old": old,
                            "new": attachment["template"].format(old_path=old)
                        })

        # build styles and
        styles_template = self.settings["PREPARATION"]["STYLES"]["template"]
        scripts_template = self.settings["PREPARATION"]["SCRIPTS"]["template"]

        styles = get_additional(index.get_page_tags('link', parent='head')['link'], styles_template)
        scripts = get_additional(index.get_page_tags("script", parent='head')['script'], scripts_template)

        page_parts = index.get_page_parts('header', 'footer')

        template_data = {
            "head_styles": styles,
            "head_scripts": scripts
        }

        # handle menu
        menu = self.settings["PREPARATION"]["REPLACEMENT"][0]
        menu_content = index.get_page_parts(menu["page-part"])[menu["page-part"]][0]
        replacement.append({"old": menu_content, "new": menu["template"]})

        # compose theme
        for key in page_parts.keys():
            page_parts[key] = page_parts[key][0]
            for i in replacement:
                page_parts[key] = page_parts[key].replace(i['old'], i['new'])

        template_data.update(page_parts)

        for name, template_file in self.templates.items():
            content = template_file.get_content()
            self.cms_theme.files[template_file.template_file_name] = content.format(**template_data)

        # add xml description
        xml_file = self.build_xml()
        self.cms_theme.files["templateDetails.xml"] = xml_file.get_content()

    def build_xml(self):
        """
        Realizes building xml file using settings. Returns XMLFile object.

        :return: XMLFile object
        """
        xml_settings = self.settings["XML_DESCRIPTION"]
        xml_file = XMLFile(path=os.path.join(self.cms_theme.path, xml_settings["path"]),
                           root_name=xml_settings["base"]["name"],
                           attributes=xml_settings["base"]["attributes"])

        for xml_tag, text in self.request_data.items():
            if xml_tag not in xml_settings["form_data"]["excluded"]:
                xml_file.add_child(".", xml_tag, text)

        for xml_tag, xml_content in xml_settings["tags"].items():
            if bool(xml_content) is False:
                xml_content = {}
            xml_file.add_child(".", xml_tag, **xml_content)

        for file in self.settings['FILES']:
            if file.startswith('language'):
                text = file.replace("language", "")
                attributes = {"tag": self.request_data["language"]}
                xml_file.add_child("languages", "language", text, attributes)

        for directory in self.uploaded_theme.directories:
            xml_file.add_child("files", "folder", directory.name)

        # get root files
        root_files = [file for file in  self.uploaded_theme.other_files
                      if os.path.relpath(self.cms_theme.path, file.path) == '..']

        for file in self.cms_theme.files.keys():
            if file == os.path.basename(file):
                root_files.append(FileObject(file))

        for file in root_files:
            xml_file.add_child("files", "filename", file.name)

        return xml_file
