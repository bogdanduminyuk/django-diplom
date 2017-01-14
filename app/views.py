from django.shortcuts import render

base_title = 'Сервис помощи Веб-разработчику'


def index(request):
    return render(request, 'app/index.html', {
        'title': base_title,
        'header': 'Главная страница'
    })


def generate_base_template(request):
    return render(request, 'app/generate_base_template.html', {
        'title': 'Генерация основного шаблона | ' + base_title,
        'header': 'Генерация основного шаблона',
        'panel_type': 'panel-primary',
        'panel_heading': 'Данные для генерации',
        'form_action': '#',
    })
