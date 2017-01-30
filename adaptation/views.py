from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import WpAdaptForm, JoomlaAdaptForm


def wordpress_adaptation(request):
    return handle_adapt_request(request, WpAdaptForm, 'WordPress')


def joomla_adaptation(request):
    return handle_adapt_request(request, JoomlaAdaptForm, 'Joomla')


def handle_adapt_request(request, form_class, form_name):
    result = {
        'title': 'Адаптация под ' + form_name,
        'page_header': 'Адаптация под ' + form_name,
        'panel_heading': 'Заполните данные для адаптации под ' + form_name,
        'panel_type': 'panel-primary',
        'submit_btn_type': 'btn-primary',
        'submit_value': 'Адаптировать',
        'form_action': '#',
        'hidden': form_name,
    }

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)

        if form.is_valid():
            cleaned_data = form.cleaned_data
            cleaned_data['file'] = form.save_file()

            redirect = HttpResponseRedirect('/result')
            request.session['form_data'] = cleaned_data
            return redirect
    else:
        form = form_class()

    result['form'] = form
    return render(request, 'base/form_common.html', result)
