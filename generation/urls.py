from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'generate_base_template/$', views.generate_base_template, name='generate_base_template'),
    url(r'generate_base_styles/$', views.generate_base_styles, name='generate_base_styles'),
]