from django.shortcuts import render
from app.forms import WpAdaptForm

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
        'panel_heading': 'Заполните данные для генерации основных стилей',
        'panel_type': 'panel-primary',
        'submit_btn_type': 'btn-primary',
        'form_action': '#',
        'submit_value': 'Генерировать',
    })


def wordpress_adaptation(request):
    return render(request, 'app/wp_adapt.html', {
        'title': 'Адаптация под WordPress | ' + base_title,
        'page_header': 'Адаптация под WordPress',
        'panel_heading': 'Заполните данные для адаптации под WordPress',
        'panel_type': 'panel-primary',
        'submit_btn_type': 'btn-primary',
        'form_action': '#',
        'submit_value': 'Адаптировать',
        'form': WpAdaptForm
    })


def joomla_adaptation(request):
    return render(request, 'app/joomla_adapt.html', {
        'title': 'Адаптация под Joomla | ' + base_title,
        'page_header': 'Адаптация под Joomla',
        'panel_heading': 'Заполните данные для адаптации под Joomla',
        'panel_type': 'panel-primary',
        'submit_btn_type': 'btn-primary',
        'form_action': '#',
        'submit_value': 'Адаптировать',
    })


def common_help(request):
    return render(request, 'app/common_help.html', {
        'title': 'Справка по проекту | ' + base_title,
        'page_header': 'Справка по проекту',
        'panel_heading': 'Общая справка по данному проекту',
        'panel_type': 'panel-info',
    })
