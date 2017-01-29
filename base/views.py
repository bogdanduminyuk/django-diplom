import os

from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from django.utils.datastructures import MultiValueDictKeyError


def home(request):
    return render(request, 'base/index.html', {
        'title': 'Сервис помощи Web-разработчику',
        'page_header': 'Главная страница'
    })


def result(request):
    try:
        request.GET['loading']
    except MultiValueDictKeyError:
        return render(request, 'base/result.html', {
            'title': 'Результат работы',
            'page_header': 'Обработка',
            'image': os.path.join(settings.STATIC_URL, 'img/loading.gif'),
        })

    else:
        import time
        time.sleep(2)

        json = {}
        image = 'img/oops.png'

        try:
            filename = request.session['filename']
        except KeyError:
            json['status'] = 'False'
        else:
            del request.session['filename']
            json['status'] = 'True'
            image = 'img/success.jpg'
            json['href'] = os.path.join(settings.MEDIA_URL, filename)
        finally:
            json['image'] = os.path.join(settings.STATIC_URL, image)
            response = JsonResponse(json)
            return response


