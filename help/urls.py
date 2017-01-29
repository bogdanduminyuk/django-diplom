from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'common/$', views.common_help, name='common_help'),
    url(r'adaptation/$', views.adaptation_help, name='adaptation_help'),
    url(r'generation/$', views.generation_help, name='generation_help'),
]