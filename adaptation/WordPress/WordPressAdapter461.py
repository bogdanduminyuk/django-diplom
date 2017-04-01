# coding: utf-8

from adaptation.WordPress.WordPressAdapter import WordPressAdapter


class WordPressAdapter461(WordPressAdapter):
    """Custom wordpress adapter"""
    def adapt(self):
        super(WordPressAdapter461, self).adapt()

        for filename, file_content in self.settings["FILES"].items():
            template = self.get_template(filename)

            if template is not None:
                file_content = template.get_content(**self.template_data)
            else:
                for key, page_part_content in self.template_data.items():
                    if filename.startswith(key):
                        file_content = page_part_content

            self.theme.add_file(filename, file_content)
