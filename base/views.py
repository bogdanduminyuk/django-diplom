import os

from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings


def home(request):
    return render(request, 'base/index.html', {
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

    # TODO: remove sleeping in production
    import time
    time.sleep(1)

    json = {}
    image = 'img/oops.png'

    try:
        form_data = request.session['form_data']
        filename = os.path.basename(form_data['file'])
    except KeyError:
        json['status'] = 'False'
    else:
        del request.session['form_data']

        json['status'] = 'True'
        image = 'img/success.jpg'
        json['href'] = os.path.join(settings.MEDIA_URL, filename)
    finally:
        json['image'] = os.path.join(settings.STATIC_URL, image)
        response = JsonResponse(json)
        return response


