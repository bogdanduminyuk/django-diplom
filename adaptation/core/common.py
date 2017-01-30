import os
import shutil

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render


def handle_adaptation(form_data):
    """
    Handler of all adaptation events.

    It is used for unpacking and packing archives of input/output data when we adapt something.
    It calls global adapt method for handle form_data and make adaptation.

    :param form_data: clean data from input form
    :return: href of archived file
    """
    src_file_path = form_data['file']
    extract_dir = os.path.splitext(src_file_path)[0]
    shutil.unpack_archive(src_file_path, extract_dir, 'zip')

    root_dir, base_dir = global_adapt(extract_dir, form_data)  # calling global adapt method.

    result_filename = os.path.join(root_dir, base_dir)
    archived_file = shutil.make_archive(result_filename, 'zip', root_dir, base_dir)
    archived_filename = os.path.basename(archived_file)

    return os.path.join(settings.MEDIA_URL, archived_filename)


def global_adapt(src_dir, form_data):
    """
    Global adaptation method.

    Detects under what data must be adapted and calls corresponding method.

    :param src_dir: source unpacked dir
    :param form_data: clean data from input form
    :return: tuple of parent dir and dir_name needed for packing result
    """
    parent_dir, src_dir_name = os.path.split(src_dir)
    dst_dir = os.path.join(parent_dir, form_data['name'])

    # TODO: here will places handling
    shutil.copytree(src_dir, dst_dir)

    return parent_dir, form_data['name']


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

            redirect = HttpResponseRedirect('/result')

            # TODO: try to send form_class with sessions
            request.session['form_data'] = cleaned_data

            return redirect
    else:
        form = form_class()

    result['form'] = form
    return render(request, 'base/form_common.html', result)
