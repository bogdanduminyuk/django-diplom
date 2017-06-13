# coding: utf-8

from adaptation.core.classes import Getter
from adaptation.core.themes import ThemesManager


class Adapter:
    """
    Class is used as interface for adaptation.

    Just call adapt-method for make adaptation.
    """
    @staticmethod
    def adapt(request_data):
        getter = Getter(request_data["form"], request_data["version"])
        settings = getter.get_settings(request_data)
        templates = getter.get_templates()
        plugin = getter.get_plugin()

        themes_manager = ThemesManager(request_data, settings, templates)
        return themes_manager.adapt(plugin)
