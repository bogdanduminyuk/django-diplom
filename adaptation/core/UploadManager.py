# coding: utf-8
import os
import shutil

from django.conf import settings


class UploadManager:
    def __init__(self, filename, theme_name):
        self.src = os.path.splitext(filename)[0]
        self.dst = os.path.join(settings.MEDIA_ROOT, theme_name)
        self.filename = filename
        self.theme_name = theme_name

        for directory in [self.src, self.dst]:
            if os.path.exists(directory):
                print("Removing dir:", directory)
                shutil.rmtree(directory)
            os.mkdir(directory)

    def __del__(self):
        for directory in [self.src, self.dst]:
            if os.path.exists(directory):
                print("Removing dir:", directory)
                shutil.rmtree(directory)

    def upload(self):
        shutil.unpack_archive(self.filename, self.src, 'zip')

        listdir = os.listdir(self.src)
        files = {}

        for file in listdir:
            abs_src = os.path.join(self.src, file)
            abs_dst = os.path.join(self.dst, file)
            name, ext = os.path.splitext(file)

            if os.path.isdir(abs_src):
                shutil.copytree(abs_src, abs_dst)
            elif ext not in ['.html', '.htm', '.php']:
                shutil.copyfile(abs_src, abs_dst)
            else:
                files[file] = {
                    'src': abs_src,
                    'dst': abs_dst,
                }

        return files

    def download(self, files):
        for path, content in files:
            abs_path = os.path.join(self.dst, path)
            with open(abs_path, "w", encoding='utf-8') as file:
                file.write(content)

        path = shutil.make_archive(self.dst, 'zip', root_dir=settings.MEDIA_ROOT, base_dir=self.theme_name)
        return os.path.join(settings.MEDIA_URL, os.path.basename(path))
