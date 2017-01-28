from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'common/$', views.common, name='common_help'),
    url(r'adaptation/$', views.adaptation, name='adaptation_help'),
    url(r'generation/$', views.generation, name='generation_help'),
]