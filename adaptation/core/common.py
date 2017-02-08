import os
import shutil
import json

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render

from adaptation.core.classes import UserFileNotFoundError, DescriptionKeyNotFoundError, AdaptationTypeError
from adaptation.core.functions import split_path
from adaptation.core.joomla import adaptation_joomla
from adaptation.core.wordpress import adaptation_wordpress
from adaptation import settings as adapt_settings


def adapt(form_data):
    """
    External adapt function. It delegates path_layer handling.

    :param form_data: data of input form
    :return: href to result archive
    """
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

    try:
        shutil.unpack_archive(input_file, archive_destination, 'zip')

        # Delegation to the files_layer
        adaptation_files_layer(archive_destination, work_dir, form_data)

        archived_file_path = shutil.make_archive(work_dir, 'zip',
                                                 root_dir=settings.MEDIA_ROOT,
                                                 base_dir=form_data['name'])
    except Exception as e:
        raise e

    finally:
        # clear tmp dir after yourself
        for directory in [archive_destination, work_dir]:
            if os.path.exists(directory):
                shutil.rmtree(directory)

    return os.path.join(settings.MEDIA_URL, os.path.basename(archived_file_path))


def adaptation_files_layer(src_dir, dst_dir, data):
    """
    Files layer handling.

    Writes dict{filename : content} to files in dst_dir.
    The dict is result of adaptation_core_level.

    :param src_dir: path to the dir of unpacked input file
    :param dst_dir: path to the destination dir that have to be created before
    :param data: data of input form and additional script data
    :return: None
    """
    def checking_requirements(src_dir):
        """
        Checks if requirements are complied.

        :param src_dir: path to the dir of unpacked input file
        :return: description dict of absolute paths of files in description
        """
        for required_file in adapt_settings.COMMON_REQUIRES_FILES:
            absolute_path = os.path.join(src_dir, required_file)

            if not os.path.exists(absolute_path):
                raise UserFileNotFoundError(required_file)

        # if description.json was found
        description_path = os.path.join(src_dir, 'description.json')
        with open(description_path, 'r', encoding='utf-8') as description_file:
            description = json.loads(description_file.read())

        for key, value in description.items():
            if key not in adapt_settings.REQUIRED_DESCRIPTION_KEYS:
                raise DescriptionKeyNotFoundError(key)
            else:
                description[key] = os.path.join(src_dir, value)

        return description

    data['description.json'] = checking_requirements(src_dir)  # it can raise exception

    files = adaptation_core_layer(src_dir, data)

    if not os.path.exists(dst_dir):
        os.mkdir(dst_dir)

    for filename, content in files.items():
        path = os.path.join(dst_dir, filename)

        with open(path, 'w+', encoding='utf-8') as file:
            file.write(content)


def adaptation_core_layer(src_dir, data):
    """
    Core adaptation handling.

    Determines what adaptation type is. It uses form type.

    :param src_dir: path to the dir of unpacked input file
    :param data: data of input form and additional script data
    :return: dict {filename : content}
    """
    form_type = data['form']

    if form_type == 'WordPress':
        call = adaptation_wordpress
    elif form_type == 'Joomla':
        call = adaptation_joomla
    else:
        raise AdaptationTypeError(form_type)

    files = call(src_dir, data)
    return files


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
