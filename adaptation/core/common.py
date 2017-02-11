from django.http import HttpResponseRedirect
from django.shortcuts import render


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

            redirect = HttpResponseRedirect('/result')

            # TODO: try to send form_class with sessions
            request.session['form_data'] = cleaned_data

            return redirect
    else:
        form = form_class()

    result['form'] = form
    return render(request, 'base/form_common.html', result)
