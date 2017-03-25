# coding: utf-8


# TODO: realize it
class Theme:
    def __init__(self, request_data, files, settings, src_path):
        self.request_data = request_data
        self.files = files
        self.settings = settings
        self.src_path = src_path

    def get_file(self, filename):
        return self.files[filename]
