from django.shortcuts import render


base_title = 'Сервис помощи Веб-разработчику'


def home(request):
    return render(request, 'base/index.html', {
        'title': base_title,
        'header': 'Главная страница'
    })


def success(request):
    return render(request, 'base/success.html')
