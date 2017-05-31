import os

from adaptation.core.file_types import TemplateFile
from adaptation import settings as adapt_settings


class BasePlugin:
    def __init__(self, uploaded_theme, cms_theme, settings, templates):
        self.uploaded_theme = uploaded_theme
        self.cms_theme = cms_theme
        self.settings = settings
        self.templates = templates

    def adapt(self):
        index = self.uploaded_theme.get_file('index.html')


