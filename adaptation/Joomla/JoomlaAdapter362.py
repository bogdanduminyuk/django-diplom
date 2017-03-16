# coding: utf-8
from adaptation.Joomla.JoomlaAdapter import JoomlaAdapter


class JoomlaAdapter362(JoomlaAdapter):
    # TODO: fix hidden slider
    # TODO: add <?php echo $template_url;?> before images, scripts, etc.
    # TODO: fix $ is not a function
    def adapt(self):
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
                    file_content = tpl_content.format(**self.data)
            else:
                file_content = content
            # here I see index_content without preparation because **self.data filled before preparation
            # TODO: fix self.data filling before preparation
            files[file] = file_content

        self.__append_files__(files)
        pretty_xml_str = self.__get_pretty_xml__(self.xml_element)
        files['templateDetails.xml'] = pretty_xml_str

        return files
