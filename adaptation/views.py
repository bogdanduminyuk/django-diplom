import os
from os.path import splitext

from django.forms import forms
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import WpAdaptForm
import base.settings as my_settings
from django.conf import settings


def wordpress_adaptation(request):
    if request.method == 'POST':
        form = WpAdaptForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']

            if uploaded_file.size > my_settings.MAX_UPLOAD_FILE_SIZE:
                raise forms.ValidationError('MAX_UPLOAD_FILE_LIMIT')

            name, ext = splitext(uploaded_file.name)
            print(uploaded_file.content_type)

            if ext != '.zip':
                raise forms.ValidationError('Found not zip extension')

            if uploaded_file.content_type not in my_settings.CONTENT_TYPES:
                raise forms.ValidationError('Wrong content-type of uploaded file')

            print(uploaded_file.content_type)
            print(uploaded_file.name)
            print(uploaded_file.size)

            dir = os.path.join(settings.BASE_DIR, 'uploads')

            try:
                os.mkdir(dir)
            except:
                pass

            filename = os.path.join(dir, uploaded_file.name)

            with open(filename, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

        else:
            print('form not valid')

            # return response
    else:
        form = WpAdaptForm()
    return render(request, 'base/form_common.html', {
        'title': 'Адаптация под WordPress',
        'page_header': 'Адаптация под WordPress',
        'panel_heading': 'Заполните данные для адаптации под WordPress',
        'panel_type': 'panel-primary',
        'submit_btn_type': 'btn-primary',
        'form_action': '#',
        'submit_value': 'Адаптировать',
        'form': form
    })


def joomla_adaptation(request):
    return render(request, 'base/form_common.html', {
        'title': 'Адаптация под Joomla',
        'page_header': 'Адаптация под Joomla',
        'panel_heading': 'Заполните данные для адаптации под Joomla',
        'panel_type': 'panel-primary',
        'submit_btn_type': 'btn-primary',
        'form_action': '#',
        'submit_value': 'Адаптировать',
    })
