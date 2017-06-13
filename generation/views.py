from django.shortcuts import render


def generate_base_template(request):
    return render(request, 'base/form_common.html', {
        'title': 'Генерация основного шаблона',
        'page_header': 'Генерация основного шаблона',
        'panel_type': 'panel-primary',
        'submit_btn_type': 'btn-primary',
        'panel_heading': 'Данные для генерации',
        'form_action': '#',
        'submit_value': 'Генерировать',
    })


def generate_base_styles(request):
    return render(request, 'base/form_common.html', {
        'title': 'Генерация шаблонных стилей',
        'page_header': 'Генерация шаблонных стилей',
        'panel_heading': 'Заполните данные для генерации основных стилей',
        'panel_type': 'panel-primary',
        'submit_btn_type': 'btn-primary',
        'form_action': '#',
        'submit_value': 'Генерировать',
    })
