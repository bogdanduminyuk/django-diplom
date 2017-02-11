# coding: utf-8
from adaptation import settings as adapt_settings


class WordPressAdapter:
    def __init__(self, description, data):
        self.description = description
        self.data = data

    def adapt(self):
        files = {}

        class_shortcut = "adapter"
        import_string = "from . import WordPressAdapter{0} as {1}".format(self.data['version'], class_shortcut)
        call_string = "{0}.WordPressAdapter{1}().adapt()".format(class_shortcut, self.data['version'])

        exec(import_string)
        version_adaptation = eval(call_string)

        src_css = self.description['css']
        styles = self.get_wp_styles(src_css)

        files.update(version_adaptation)
        files.update(styles)

        return files

    def get_wp_styles(self, source_css_file):
        """
        Gets content of input css remade to wp.

        :param source_css_file: path to source css
        :return: wp css content
        """
        with open(source_css_file, 'r', encoding='utf-8') as styles_file:
            content = adapt_settings.WORDPRESS['STYLE']['CONTENT'].format(
                self.data['name'],
                self.data.get('author', ''),
                self.data.get('description', ''),
                self.data['version'],
                self.data.get('theme_license', ''),
                self.data.get('tags', ''),
                self.data.get('comments', ''),
                styles_file.read()
            )

            return {adapt_settings.WORDPRESS['STYLE']['FILE']: content}
