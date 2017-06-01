

class BasePlugin:
    def __init__(self, uploaded_theme, cms_theme, settings, templates, request_data):
        self.uploaded_theme = uploaded_theme
        self.cms_theme = cms_theme
        self.settings = settings
        self.templates = templates
        self.request_data = request_data
