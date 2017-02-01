import os
import shutil

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render

from adaptation.core.functions import split_path


def adapt(form_data):
    """External adapt function. It delegates path_layer handling"""
    return adaptation_path_layer(form_data)


def adaptation_path_layer(form_data):
    """
    Path layer handling.

    Realizes working with paths, packing/unpacking archives, cutting and joining paths, creation of dirs.
    It delegates files_layer handling.

    :param form_data: data of input form
    :return: href to result archive
    """
    input_file = form_data['file']
    folder, filename, ext = split_path(input_file)

    archive_destination = os.path.join(settings.TEMP_DIR, filename)
    work_dir = os.path.join(settings.MEDIA_ROOT, form_data['name'])

    shutil.unpack_archive(input_file, archive_destination, 'zip')

    # Delegation to the files_layer
    adaptation_files_layer(archive_destination, work_dir, form_data)

    archived_file_path = shutil.make_archive(work_dir, 'zip', root_dir=settings.MEDIA_ROOT, base_dir=form_data['name'])

    # clear tmp dir after yourself
    for directory in [archive_destination, work_dir]:
        shutil.rmtree(directory)

    return os.path.join(settings.MEDIA_URL, os.path.basename(archived_file_path))


def adaptation_files_layer(src_dir, dst_dir, form_data):
    """
    Files layer handling.

    :param src_dir: path to the dir of unpacked input file
    :param dst_dir: path to the destination dir that have to be created before
    :param form_data: data of input form
    :return: None
    """
    # TODO: it do something with files.
    shutil.copytree(src_dir, dst_dir)


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
