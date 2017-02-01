import os

from django.conf import settings
from django.http import HttpResponse

from .forms import WpAdaptForm, JoomlaAdaptForm
from adaptation.core.common import handle_adapt_request, global_adapt, handle_adaptation


def wordpress_adaptation(request):
    return handle_adapt_request(request, WpAdaptForm, 'WordPress')


def joomla_adaptation(request):
    return handle_adapt_request(request, JoomlaAdaptForm, 'Joomla')


def test(request):
    get_dict = request.GET.dict()

    file_name = get_dict.get('file', 'snowboarding')
    file = file_name + '.zip'
    example = os.path.join(settings.BASE_DIR, 'examples', 'wp', file_name)

    form_data = {'name': file, 'file': example}

    result_href = handle_adaptation(form_data)

    return HttpResponse('<a href="' + result_href + '">Скачать</a>')
