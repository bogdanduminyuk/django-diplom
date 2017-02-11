# coding: utf-8
from adaptation.WordPress.WordPressAdapter import WordPressAdapter


class WordPressAdapter461(WordPressAdapter):
    def adapt(self):
        files = {}

        styles = self.get_wp_styles(self.description['css'])

        files.update(styles)

        return files
