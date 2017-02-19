# coding: utf-8
from adaptation.core.UploadManager import UploadManager


class Adapter:
    """
    Class is used as interface for adaptation.

    Just call adapt-method for make adaptation.
    """
    def __init__(self, data):
        self.data = data
        self.upload_manager = UploadManager(data['file'], data['name'])

    def adapt(self):
        files_to_work = self.upload_manager.upload()

        package = self.data['form']
        adapter_class = '{0}Adapter{1}'.format(self.data['form'], self.data['version'])
        import_string = 'import adaptation.{0}.{1} as adapter'.format(package, adapter_class)
        call_string = 'adapter.{0}(files_to_work, self.data).adapt()'.format(adapter_class)

        exec(import_string)
        files = eval(call_string)

        return self.upload_manager.download(files)
