from django.shortcuts import render
from .forms import WpAdaptForm


def wordpress_adaptation(request):
    return render(request, 'base/form_common.html', {
        'title': 'Адаптация под WordPress',
        'page_header': 'Адаптация под WordPress',
        'panel_heading': 'Заполните данные для адаптации под WordPress',
        'panel_type': 'panel-primary',
        'submit_btn_type': 'btn-primary',
        'form_action': '#',
        'submit_value': 'Адаптировать',
        'form': WpAdaptForm
    })