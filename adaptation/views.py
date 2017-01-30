from .forms import WpAdaptForm, JoomlaAdaptForm
from adaptation.core.common import handle_adapt_request


def wordpress_adaptation(request):
    return handle_adapt_request(request, WpAdaptForm, 'WordPress')


def joomla_adaptation(request):
    return handle_adapt_request(request, JoomlaAdaptForm, 'Joomla')
