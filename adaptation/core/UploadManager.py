# coding: utf-8
import os
import shutil
import distutils.dir_util as dir_util

from django.conf import settings


class UploadManager:
    def __init__(self, filename, theme_name):
        self.src = os.path.join(settings.TEMP_DIR, os.path.splitext(os.path.basename(filename))[0])
        self.dst = os.path.join(settings.MEDIA_ROOT, theme_name)
        self.filename = filename
        self.theme_name = theme_name

        print("Src:", self.src)
        print("Dst:", self.dst)
        print("Filename:", self.filename)
        print("Theme name:", self.theme_name)

        for directory in [self.src, self.dst]:
            if os.path.exists(directory):
                print("Removing dir:", directory)
                shutil.rmtree(directory)
            print("Creating dir:", directory)
            os.mkdir(directory)

    def __del__(self):
        for directory in [self.src, self.dst]:
            if os.path.exists(directory):
                print("Removing dir:", directory)
                shutil.rmtree(directory)

    def upload(self):
        shutil.unpack_archive(self.filename, self.src, 'zip')

        listdir = os.listdir(self.src)
        files = {
            "moved": {},
            "other": {},
        }

        for file in listdir:
            abs_src = os.path.join(self.src, file)
            abs_dst = os.path.join(self.dst, file)
            name, ext = os.path.splitext(file)

            if os.path.isdir(abs_src):
                shutil.copytree(abs_src, abs_dst)
                files['moved'][file] = "folder"
            elif ext not in ['.html', '.htm', '.php']:
                shutil.copyfile(abs_src, abs_dst)
                files['moved'][file] = "filename"
            else:
                files['other'][file] = {
                    'src': abs_src,
                    'dst': abs_dst,
                }

        return files

    def download(self, files):
        dir_util.create_tree(self.dst, files)
        for path, content in files.items():
            abs_path = os.path.join(self.dst, path)
            with open(abs_path, "w", encoding='utf-8') as file:
                file.write(content)

        path = shutil.make_archive(self.dst, 'zip', root_dir=settings.MEDIA_ROOT, base_dir=self.theme_name)
        return os.path.join(settings.MEDIA_URL, os.path.basename(path))
