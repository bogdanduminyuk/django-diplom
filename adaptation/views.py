import datetime
import os

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

from adaptation.conflicts.classes import ConflictChecker
from adaptation.core.adapters import Adapter
from adaptation.core.classes import Getter
from adaptation.core.functions import handle_adapt_request
from adaptation.core.themes import UploadedTheme
from .forms import WpAdaptForm, JoomlaAdaptForm, ConflictsForm


def wordpress_adaptation(request):
    return handle_adapt_request(request, WpAdaptForm, 'WordPress')


def joomla_adaptation(request):
    return handle_adapt_request(request, JoomlaAdaptForm, 'Joomla')


def wp_test(request):
    get_dict = request.GET.dict()

    file_name = get_dict.get('file', 'snowboarding')
    file = file_name + '.zip'
    example = os.path.join(settings.BASE_DIR, 'examples', 'wp', file)

    form_data = {
        'name': file_name,
        'file': example,
        'form': 'WordPress',
        'version': 461,
        'author': '',
        'description': '',
        'license': '',
        'tags': '',
        'comments': '',
    }

    adapter = Adapter()
    result_href = adapter.adapt(form_data)

    return HttpResponse('<a href="' + result_href + '">Скачать</a>')


def joomla_test(request):
    get_dict = request.GET.dict()

    file_name = get_dict.get('file', 'snowboarding')
    file = file_name + '.zip'
    example = os.path.join(settings.BASE_DIR, 'examples', 'wp', file)

    form_data = {
        'name': file_name,
        'file': example,
        'form': 'Joomla',
        'version': 362,
        'language': 'en-GB',
        'creationDate': datetime.datetime.now().strftime("%d-%m-%Y"),
        'author': '',
        'authorEmail': '',
        'copyright': '',
        'license': '',
        'authorUrl': '',
    }

    adapter = Adapter()
    result_href = adapter.adapt(form_data)

    return HttpResponse('<a href="' + result_href + '">Скачать</a>')


def conflicts_test(request):
    file = os.path.join(settings.BASE_DIR, 'examples', 'wp', 'snowboarding.zip')
    cfg = Getter.get_user_cfg()["CONFLICTS"]
    checker = ConflictChecker()
    theme = UploadedTheme(file, 'conflicts')
    theme.unpack()
    theme.read_files()
    index_file = theme.get_file('index.html')
    scripts = {
        "functions": cfg.get('functions_script', '')
    }

    return render(request, 'base/conflicts_result.html', {
        'result': checker.check(index_file.path, scripts, cfg.get('urls')),
        'title': "Поиск конфликтов",
        'page_header': "Результаты проверки"
    })


def conflicts(request):
    if request.method == 'POST':
        form = ConflictsForm(request.POST, request.FILES)
        file = form.save_file()
        cfg = Getter.get_user_cfg()["CONFLICTS"]

        if request.POST.get('use_defaults', '') != 'on':
            cfg['urls']['wordpress_url'] = request.POST['wordpress_url']
            cfg['urls']['joomla_url'] = request.POST['joomla_url']

        checker = ConflictChecker()
        theme = UploadedTheme(file, 'conflicts')
        theme.unpack()
        theme.read_files()
        index_file = theme.get_file('index.html')

        scripts = {
            "functions": cfg.get('functions_script', ''),
            # "styles": cfg.get('styles_script', '')
        }

        result = checker.check(index_file.path, scripts, cfg.get('urls'))

        return render(request, 'base/conflicts_result.html', {
            'result': result,
            'title': "Поиск конфликтов",
            'page_header': "Результаты проверки"
        })

    else:
        return render(request, 'base/conflicts.html', {
            'title': "Поиск конфликтов",
            "page_header": "Поиск конфликтов",
            'panel_heading': 'Проверьте данные проверки конфликтов',
            'panel_type': 'panel-info',
            'submit_btn_type': 'btn-outline btn-warning',
            'submit_value': 'Проверить',
            'form_action': '#',
            'hidden': 'conflict',
            'form': ConflictsForm
        })