# coding: utf-8
import os

from adaptation.Joomla.JoomlaAdapter import JoomlaAdapter


class JoomlaAdapter362(JoomlaAdapter):
    def adapt(self, **kwargs):
        super(JoomlaAdapter362, self).adapt(**kwargs)

        for filename, content in self.settings["FILES"].items():
            if content == "{content}":
                template_name = os.path.basename(filename) + ".tpl"

                if template_name in self.templates.keys():
                    content = self.templates[template_name].get_content(**self.template_data)

            self.theme.add_file(os.path.join(self.theme.dst_dir, filename), content)

        xml_file = self.build_xml()
        self.theme.add_file(xml_file.wpath, xml_file.get_content())
