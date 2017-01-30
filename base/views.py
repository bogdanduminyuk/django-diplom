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

    # TODO: remove sleeping in production
    import time
    time.sleep(1)

    json = {}
    image = 'img/oops.png'

    try:
        form_data = request.session['form_data']
        file_path = form_data['file']
        file_name = os.path.basename(file_path)
    except KeyError:
        json['status'] = 'False'
    else:
        del request.session['form_data']

        result_file_path = handle_adaptation(form_data)
        result_file = os.path.basename(result_file_path)

        json['href'] = os.path.join(settings.MEDIA_URL, result_file)

        image = 'img/success.jpg'
        json['status'] = 'True'
    finally:
        json['image'] = os.path.join(settings.STATIC_URL, image)
        response = JsonResponse(json)
        return response


def handle_adaptation(form_data):
    src_file_path = form_data['file']

    src_basename = os.path.basename(src_file_path)
    extract_dir = os.path.join(settings.MEDIA_ROOT, src_basename.split('.')[0])

    shutil.unpack_archive(src_file_path, extract_dir, 'zip')

    # TODO: here do_stuff places...
    root_dir, base_dir = do_stuff(extract_dir, form_data)

    return shutil.make_archive(os.path.join(root_dir, form_data['name']),
                               'zip',
                               root_dir=root_dir,
                               base_dir=base_dir)


def do_stuff(src_dir, form_data):
    root_dir, base_dir = os.path.split(src_dir)

    # TODO: do stuff...

    return root_dir, base_dir
