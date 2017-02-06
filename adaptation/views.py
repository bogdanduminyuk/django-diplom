import os

from django.conf import settings
from django.http import HttpResponse

from .forms import WpAdaptForm, JoomlaAdaptForm
from adaptation.core.common import handle_adapt_request, adapt


def wordpress_adaptation(request):
    return handle_adapt_request(request, WpAdaptForm, 'WordPress')


def joomla_adaptation(request):
    return handle_adapt_request(request, JoomlaAdaptForm, 'Joomla')


def test(request):
    get_dict = request.GET.dict()

    file_name = get_dict.get('file', 'snowboarding')
    file = file_name + '.zip'
    example = os.path.join(settings.BASE_DIR, 'examples', 'wp', file)

    form_data = {'name': file_name, 'file': example, 'form': 'WordPress', 'version': 461}

    result_href = adapt(form_data)

    return HttpResponse('<a href="' + result_href + '">Скачать</a>')
