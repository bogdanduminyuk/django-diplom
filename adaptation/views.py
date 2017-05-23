import datetime
import os
import pprint

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

from adaptation.core.adapters import Adapter
from adaptation.core.functions import handle_adapt_request
from conflicts.classes import SeleniumPhantomJSDriver
from core.classes import Getter, Uploader
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

    adapter = Adapter(form_data)
    result_href = adapter.adapt()

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

    adapter = Adapter(form_data)
    result_href = adapter.adapt()

    return HttpResponse('<a href="' + result_href + '">Скачать</a>')


def conflicts(request):
    if request.method == 'POST':
        form = ConflictsForm(request.POST, request.FILES)
        file = form.save_file()
        cfg = Getter.get_user_cfg()["CONFLICTS"]

        if request.POST.get('use_defaults', '') != 'on':
            cfg['wordpress_url'] = request.POST['wordpress_url']
            cfg['joomla_url'] = request.POST['joomla_url']

        driver = SeleniumPhantomJSDriver()
        theme = Uploader().upload(file, 'conflicts')
        theme.read_files()
        index_file = theme.get_file('index.html')
        result = {}

        for key, url in cfg['urls'].items():
            result[key] = driver.execute_script(url, cfg["script"])

        result['theme'] = driver.execute_script(index_file.rpath, cfg["script"])

        return HttpResponse("<pre>" + pprint.pformat(result) + "</pre>")

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