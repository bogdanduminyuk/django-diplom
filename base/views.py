import os

from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from django.utils.datastructures import MultiValueDictKeyError


def home(request):
    return render(request, 'base/index.html', {
        'title': 'Сервис помощи Web-разработчику',
        'header': 'Главная страница'
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
            filename = os.path.basename(request.COOKIES['filename'])
        except MultiValueDictKeyError:
            json['status'] = 'False'
        else:
            json['status'] = 'True'
            image = 'img/success.jpg'
            json['href'] = os.path.join(settings.MEDIA_URL, filename)
        finally:
            json['image'] = os.path.join(settings.STATIC_URL, image)
            response = JsonResponse(json)
            response.delete_cookie('filename')
            return response


