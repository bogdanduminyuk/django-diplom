from django.shortcuts import render


def index(request):
    return render(request, 'app/index.html', {'title': 'Сервис помощи Веб-разработчику'})
