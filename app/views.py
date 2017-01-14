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
        'page_header': 'Генерация основного шаблона',
        'panel_type': 'panel-primary',
        'submit_btn_type': 'btn-primary',
        'panel_heading': 'Данные для генерации',
        'form_action': '#',
        'submit_value': 'Адаптировать',
    })


def generate_base_styles(request):
    return render(request, 'app/generate_base_styles.html', {
        'title': 'Генерация шаблонных стилей | ' + base_title,
        'page_header': 'Генерация шаблонных стилей',
        'panel_heading': 'Заполните даные для генерации основных стилей',
        'panel_type': 'panel-primary',
        'submit_btn_type': 'btn-primary',
        'form_action': '#',
        'submit_value': 'Генерировать',
    })
