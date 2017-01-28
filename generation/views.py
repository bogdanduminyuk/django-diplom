from django.shortcuts import render


def generate_base_template(request):
    return render(request, 'generation/generate_base_template.html', {
        'title': 'Генерация основного шаблона',
        'page_header': 'Генерация основного шаблона',
        'panel_type': 'panel-primary',
        'submit_btn_type': 'btn-primary',
        'panel_heading': 'Данные для генерации',
        'form_action': '#',
        'submit_value': 'Адаптировать',
    })
