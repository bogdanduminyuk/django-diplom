import os
import shutil

from adaptation.core.file_types import DirectoryObject, FileObject, ParsableFile
from diplom import settings


class Theme:
    def __init__(self, path, name):
        self.path = path
        self.name = name

        if os.path.exists(self.path):
            shutil.rmtree(self.path)

        os.mkdir(self.path)

    def remove(self):
        if os.path.exists(self.path):
            shutil.rmtree(self.path)


class UploadedTheme(Theme):
    def __init__(self, archive_path, name):
        path = os.path.join(settings.TEMP_DIR, name)

        super().__init__(path, name)

        self.archive_path = archive_path

        self.directories = []
        self.other_files = []
        self.parsable_files = {}

    def unpack(self):
        """Realizes unpacking of the theme archive to src_dir folder."""
        shutil.unpack_archive(self.archive_path, self.path, 'zip')
        return self.path

    def read_files(self):
        """Reads files from disk (from self.path) into File Objects."""
        listdir = os.listdir(self.path)
        for file in listdir:
            abs_src = os.path.join(self.path, file)
            ext = os.path.splitext(file)[1]

            if os.path.isdir(abs_src):
                self.directories.append(DirectoryObject(abs_src))
            elif ext not in ['.html', '.htm', '.php']:
                self.other_files.append(FileObject(abs_src))
            else:
                file = ParsableFile(abs_src)
                self.parsable_files[file.name] = file
                file.read()

    def get_file(self, filename):
        return self.parsable_files.get(filename, None)


class CMSTheme(Theme):
    def __init__(self, name):
        path = os.path.join(settings.MEDIA_ROOT, name)

        super().__init__(path, name)

        self.files = {}

    def init(self, config, uploaded_theme):
        self.files = config["FILES"]

        for item in uploaded_theme.directories + uploaded_theme.other_files:
            item.copy(self.path)

    def pack(self):
        """Realizes packing of the dst_dir folder."""
        path = shutil.make_archive(self.path, 'zip', root_dir=settings.MEDIA_ROOT, base_dir=self.name)
        return os.path.join(settings.MEDIA_URL, os.path.basename(path))

    def write(self):
        for filename, content in self.files.items():
            file = FileObject(os.path.join(self.path, filename))
            file.put_content(content)


class ThemesManager:
    def __init__(self, request_data, config, templates):
        self.request_data = request_data
        self.config = config
        self.templates = templates

        name = request_data['name']

        self.uploaded_theme = UploadedTheme(request_data['file'], name)
        self.cms_theme = CMSTheme(name)

    def adapt(self, PluginClass):
        try:
            self.uploaded_theme.unpack()
            self.uploaded_theme.read_files()
            self.cms_theme.init(self.config, self.uploaded_theme)

            plugin_object = PluginClass(self.uploaded_theme,
                                        self.cms_theme,
                                        self.config,
                                        self.templates,
                                        self.request_data)
            plugin_object.adapt()

            self.cms_theme.write()
            return self.cms_theme.pack()

        finally:
            self.uploaded_theme.remove()
            self.cms_theme.remove()
