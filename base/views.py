import os
import shutil

from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings


def home(request):
    return render(request, 'base/index.html', {
        'title': 'Сервис помощи Web-разработчику',
        'page_header': 'Главная страница'
    })


def result(request):
    try:
        request.GET['loading']
    except KeyError:
        return render(request, 'base/result.html', {
            'title': 'Результат работы',
            'page_header': 'Обработка',
            'image': os.path.join(settings.STATIC_URL, 'img/loading.gif'),
        })

    json = {'image': 'img/oops.png'}

    try:
        form_data = request.session['form_data']

    except KeyError:
        json['status'] = 'False'

    else:
        del request.session['form_data']

        if 'file' in form_data:
            result_file_path = handle_adaptation(form_data)
            result_file = os.path.basename(result_file_path)
        else:
            # TODO: handle generation
            result_file = 'file'

        json['href'] = os.path.join(settings.MEDIA_URL, result_file)
        json['image'] = 'img/success.jpg'
        json['status'] = 'True'

    finally:
        json['image'] = os.path.join(settings.STATIC_URL, json['image'])
        response = JsonResponse(json)
        return response


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
