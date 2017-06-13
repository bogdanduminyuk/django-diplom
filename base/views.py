# coding: utf-8
import os

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render

from adaptation.core.adapters import Adapter


def home(request):
    return render(request, 'base/main_page.html', {
        'title': 'Сервис помощи Web-разработчику',
        'page_header': 'Главная страница'
    })


def result(request):
    try:
        request.GET['loading']
    except KeyError:
        return render(request, 'base/result.html', {
            'title': 'Результат работы',
            'page_header': 'Обработка',
            'image': os.path.join(settings.STATIC_URL, 'img/loading.gif'),
        })

    json = {'image': 'img/oops.png'}

    try:
        form_data = request.session['form_data']

    except KeyError:
        json['status'] = 'False'

    else:
        del request.session['form_data']

        if 'file' in form_data:
            adapter = Adapter()
            try:
                result_href = adapter.adapt(form_data.copy())
            except Exception as e:
                json['status'] = 'False'
                json['error'] = str(e)
        else:
            # TODO: handle generation
            result_href = 'file'

        json['href'] = result_href
        json['image'] = 'img/success.jpg'
        json['status'] = 'True'

    finally:
        json['image'] = os.path.join(settings.STATIC_URL, json['image'])
        response = JsonResponse(json)
        return response
