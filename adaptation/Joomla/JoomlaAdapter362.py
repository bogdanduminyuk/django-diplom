# coding: utf-8
import os

from adaptation.Joomla.JoomlaAdapter import JoomlaAdapter


class JoomlaAdapter362(JoomlaAdapter):
    # TODO: fix hidden slider
    # TODO: fix $ is not a function
    def adapt(self):
        super(JoomlaAdapter362, self).adapt()
        files = {}

        templates = self.templates
        settings_files = self.settings["FILES"]

        for file, content in settings_files.items():
            file_content = ''
            if file == 'templateDetails.xml':
                pass

            elif content == "{content}":
                template_name = file + '.tpl'

                # apply data to content-template
                if template_name in templates.keys():
                    tpl_content = templates[template_name]["content"]
                    file_content = tpl_content.format(**self.format_data)
            else:
                file_content = content

            files[file] = file_content

        for filename in files.keys():
            if os.path.basename(filename) == filename:
                self.xml_file.add_child("files", "filename", filename)

        files['templateDetails.xml'] = self.xml_file.prettify()

        return files
