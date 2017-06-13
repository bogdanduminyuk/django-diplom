from adaptation.core import functions
from adaptation.plugins import BasePlugin


class BaseWordPressPlugin(BasePlugin):
    def adapt(self):
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

        # fill page_parts
        index_content = index.get_content('str')
        parts = index.get_page_parts('header', 'footer')
        header = parts["header"][0]
        footer = parts["footer"][0]

        header_end_pos = index_content.find(header) + len(header)
        footer_start_pos = index_content.find(footer)

        header = index_content[0: header_end_pos]
        footer = index_content[footer_start_pos:]
        content = index_content[header_end_pos: footer_start_pos]

        page_parts = index.get_page_parts()
        page_parts.update({
            "header": header,
            "footer": footer,
            "index_content": content
        })

        for part, content in page_parts.items():
            if isinstance(content, list):
                page_parts[part] = content[0]

        # handle menu
        menu = self.settings["PREPARATION"]["REPLACEMENT"][0]
        old = index.get_page_parts(menu["page-part"], as_string=False)[menu["page-part"]][0]
        attrs = old.attrs
        params = menu["params"].format(**{
            "menu_name": attrs["name"],
            "menu_class": ' '.join(attrs["class"]),
            "menu_id": attrs["id"]
        })

        new = menu["template"].format(params=params)
        replacement.append({"old": str(old), "new": new})

        # compose theme
        template_data = self.request_data.copy()

        for key in page_parts.keys():
            for i in replacement:
                page_parts[key] = page_parts[key].replace(i['old'], i['new'])

        template_data.update(page_parts)

        for name, template_file in self.templates.items():
            content = template_file.get_content()
            self.cms_theme.files[template_file.template_file_name] = content.format(**template_data)

        self.cms_theme.files['header.php'] = template_data['header']
        self.cms_theme.files['footer.php'] = template_data['footer']
