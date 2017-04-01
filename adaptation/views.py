import datetime
import os

from django.conf import settings
from django.http import HttpResponse

from adaptation.core.adapters import Adapter
from adaptation.core.functions import handle_adapt_request
from .forms import WpAdaptForm, JoomlaAdaptForm


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
