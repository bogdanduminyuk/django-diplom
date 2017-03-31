# coding: utf-8
import os

from adaptation.Joomla.JoomlaAdapter import JoomlaAdapter

# TODO: fix that file

class JoomlaAdapter362(JoomlaAdapter):
    # TODO: fix hidden slider
    # TODO: fix $ is not a function
    def adapt(self, **kwargs):
        super(JoomlaAdapter362, self).adapt(**kwargs)
        files = {}

        for filename, content in self.settings["FILES"].items():
            basename = os.path.basename(filename)
            file = self.theme.get_file(basename)

            if file is None:
                if file is not 'templateDetails.xml':
                    file = ReadableWritableFile("", os.path.join(self.theme.dst_dir, filename))
                    file.content = content
                    self.theme.add_writable_file(file)
            elif content == "{content}":
                template_name = basename + ".tpl"

                # apply data to content-template
                if template_name in self.templates.keys():
                    tpl_content = self.templates[template_name]["content"]
                    file_content = tpl_content.format(**self.format_data)
            else:
                file_content = content

            files[filename] = file_content

        for filename in files.keys():
            if os.path.basename(filename) == filename:
                self.xml_file.add_child("files", "filename", filename)

        files['templateDetails.xml'] = self.xml_file.prettify()

        return files
