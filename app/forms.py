
from app.widgets import *


class WpAdaptForm(forms.Form):
    file = forms.FileField(label='Выберите архив с файлами html *', required=True)
    name = forms.CharField(label='Название темы *',
                           widget=CustomTextInput(),
                           required=True)

    author = forms.CharField(label='Автор', widget=CustomTextInput())
    description = forms.CharField(label='Описание', widget=CustomTextArea((3, 0)))

    version = forms.ChoiceField(label='Версия',
                                choices=(('1', 'Option 1'),('2', 'Option 2'),),
                                widget=forms.Select(attrs={'class': 'form-control'}),
                                required=True)

    theme_license = forms.CharField(label='Лицензия', widget=CustomTextArea((3, 0)))
    tags = forms.CharField(label='Теги', widget=CustomTextInput())
    comments = forms.CharField(label='Комментарии', widget=CustomTextArea((3, 0)))
