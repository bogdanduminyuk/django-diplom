import os

from base.widgets import *
from django.conf import settings


class WpAdaptForm(forms.Form):
    file = forms.FileField(label='Выберите архив с файлами html *',
                           max_length=60,
                           required=True)

    name = forms.CharField(label='Название темы *',
                           widget=CustomTextInput(),
                           required=True)

    author = forms.CharField(label='Автор',
                             widget=CustomTextInput(),
                             required=False)

    description = forms.CharField(label='Описание',
                                  widget=CustomTextArea((3, 0)),
                                  required=False)

    version = forms.ChoiceField(label='Версия *',
                                choices=(('1', 'Option 1'), ('2', 'Option 2'),),
                                widget=forms.Select(attrs={'class': 'form-control'}))

    theme_license = forms.CharField(label='Лицензия',
                                    widget=CustomTextArea((3, 0)),
                                    required=False)

    tags = forms.CharField(label='Теги',
                           widget=CustomTextInput(),
                           required=False)

    comments = forms.CharField(label='Комментарии',
                               widget=CustomTextArea((3, 0)),
                               required=False)

    def is_valid(self):
        valid = super(WpAdaptForm, self).is_valid()

        if not valid:
            return valid

        file = self.files['file']

        if file.size > settings.MAX_UPLOAD_FILE_SIZE:
            self.add_error('file', 'MAX_UPLOAD_FILE_LIMIT')
            valid = False

        if file.content_type not in settings.CONTENT_TYPES:
            self.add_error('file', 'Wrong content-type of uploaded file')
            valid = False

        name, ext = os.path.splitext(file.name)
        if ext not in settings.FILE_EXTENSIONS:
            self.add_error('file', '\'.zip\' extension is not found')
            valid = False

        return valid

    def save_file(self):
        file = self.files['file']

        try:
            os.mkdir(settings.MEDIA_ROOT)
        except FileExistsError:
            pass

        filename = os.path.join(settings.MEDIA_ROOT, file.name)

        with open(filename, "wb+") as destination:
            for chunk in file.chunks():
                destination.write(chunk)

            return filename
