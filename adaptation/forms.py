import os

from base.widgets import *
from django.conf import settings


class BaseForm(forms.Form):
    file = forms.FileField(label='Выберите архив с файлами html *',
                           max_length=60, required=True)

    name = forms.CharField(label='Название темы *',
                           widget=CustomTextInput(), required=True)

    author = forms.CharField(label='Автор',
                             widget=CustomTextInput(), required=False)

    def is_valid(self):
        valid = super(BaseForm, self).is_valid()

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
        filename = os.path.join(settings.MEDIA_ROOT, file.name)

        with open(filename, "wb+") as destination:
            for chunk in file.chunks():
                destination.write(chunk)

            return filename


class WpAdaptForm(BaseForm):
    description = forms.CharField(label='Описание',
                                  widget=CustomTextArea((3, 0)), required=False)

    version = forms.ChoiceField(label='Версия *',
                                choices=((461, '4.6.1'), (0, 'Blank record'),),
                                widget=forms.Select(attrs={'class': 'form-control'}))

    license = forms.CharField(label='Лицензия', required=False,
                                    widget=CustomTextArea((3, 0)))

    tags = forms.CharField(label='Теги', required=False,
                           widget=CustomTextInput())

    comments = forms.CharField(label='Комментарии', required=False,
                               widget=CustomTextArea((3, 0)))


class JoomlaAdaptForm(BaseForm):
    authorUrl = forms.URLField(label='URL автора', required=False,
                               widget=forms.URLInput(attrs={'class': 'form-control'}))

    authorEmail = forms.EmailField(label='Email автора', required=False,
                                   widget=forms.EmailInput(attrs={'class': 'form-control'}))

    language = forms.CharField(label='Язык', widget=CustomTextInput())

    version = forms.ChoiceField(label='Версия *',
                                choices=((362, '3.6.2'), (0, 'Blank record'),),
                                widget=forms.Select(attrs={'class': 'form-control'}))

    license = forms.CharField(label='Лицензия', required=False,
                                    widget=CustomTextArea((3, 0)))

    copyright = forms.CharField(label='Copyright', required=False,
                                      widget=CustomTextArea((3, 0)))


class ConflictsForm(forms.Form):
    wordpress_url = forms.URLField(label='URL запроса WordPress',
                                   widget=forms.URLInput(attrs={'class': 'form-control'}))

    joomla_url = forms.URLField(label='URL запроса Joomla',
                                widget=forms.URLInput(attrs={'class': 'form-control'}))

    use_defaults = forms.BooleanField(label='Использовать URL по умолчанию', required=False)

    use_cache = forms.BooleanField(label='Использовать кэш', required=False)
