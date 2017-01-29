from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import WpAdaptForm


def wordpress_adaptation(request):
    result = {
        'title': 'Адаптация под WordPress',
        'page_header': 'Адаптация под WordPress',
        'panel_heading': 'Заполните данные для адаптации под WordPress',
        'panel_type': 'panel-primary',
        'submit_btn_type': 'btn-primary',
        'submit_value': 'Адаптировать',
        'form_action': '#',
    }

    if request.method == 'POST':
        form = WpAdaptForm(request.POST, request.FILES)

        if form.is_valid():
            filename = form.save_file()
            url = reverse('result')
            redirect = HttpResponseRedirect(url)
            redirect.set_cookie('filename', filename)
            return redirect
        else:
            print('form not valid')
    else:
        form = WpAdaptForm()

    result['form'] = form
    return render(request, 'base/form_common.html', result)


def joomla_adaptation(request):
    return render(request, 'base/form_common.html', {
        'title': 'Адаптация под Joomla',
        'page_header': 'Адаптация под Joomla',
        'panel_heading': 'Заполните данные для адаптации под Joomla',
        'panel_type': 'panel-primary',
        'submit_btn_type': 'btn-primary',
        'form_action': '#',
        'submit_value': 'Адаптировать',
    })
