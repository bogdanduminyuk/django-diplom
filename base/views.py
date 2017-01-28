import os

from django.shortcuts import render
from django.conf import settings


def home(request):
    return render(request, 'base/index.html', {
        'title': 'Сервис помощи Web-разработчику',
        'header': 'Главная страница'
    })


def success(request):
    filename = os.path.basename(request.COOKIES['filename'])
    return render(request, 'base/success.html', {
        'link': os.path.join(settings.MEDIA_URL, filename)
    })

