# coding: utf-8
import datetime

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.http import HttpResponseRedirect
from django.shortcuts import render


def is_url(string):
    """
    Checks if the string is url.

    :param string: string that can be url
    :return: True if string if url and False otherwise
    """
    validator = URLValidator()
    valid = True

    try:
        validator(string)
    except ValidationError:
        valid = False

    return valid


def handle_adapt_request(request, form_class, form_name):
    """
    Common method for handling adaptation requests.

    If there is a POST-request it redirect user to 'loading' page.
    Otherwise it loads custom form.

    :param request: http-request
    :param form_class: class of requested form. Used for getting data correctly if POST and for creation otherwise.
    :param form_name: label of page (e.g. 'WordPress', 'Joomla', etc.). Used in otherwise case.
    :return: if POST HttpResponseRedirect else render-method.
    """
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
            cleaned_data['form'] = form_name
            cleaned_data['creationDate'] = datetime.datetime.now().strftime("%d-%m-%Y")

            redirect = HttpResponseRedirect('/result')
            request.session['form_data'] = cleaned_data

            return redirect
    else:
        form = form_class()

    result['form'] = form
    return render(request, 'base/form_common.html', result)
