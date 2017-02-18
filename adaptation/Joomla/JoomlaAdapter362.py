# coding: utf-8
from adaptation.Joomla.JoomlaAdapter import JoomlaAdapter


class JoomlaAdapter362(JoomlaAdapter):
    # TODO: add parse index file
    def adapt(self):
        files = {}

        templates = self.description["PRIVATE"]["TEMPLATES"]
        settings_files = self.description["PRIVATE"]["SETTINGS"]["FILES"]

        for file, content in settings_files.items():
            if content == "{content}":
                template_name = file + '.tpl'
                if template_name in templates.keys():
                    with open(templates[template_name]['path'], 'r', encoding='utf-8') as template_file:
                        tpl_content = template_file.read()
                        file_content = tpl_content.format(**self.data)
                else:
                    file_content = ''

                files[file] = file_content

        return files
