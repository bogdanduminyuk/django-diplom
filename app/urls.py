# coding: utf-8

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'generate_base_template', views.generate_base_template, name='generate_base_template'),
    url(r'generate_base_styles', views.generate_base_styles, name='generate_base_styles'),
    url(r'wordpress_adaptation', views.wordpress_adaptation, name='wordpress_adaptation'),
    url(r'joomla_adaptation', views.joomla_adaptation, name='joomla_adaptation'),
    url(r'common_help', views.common_help, name='common_help'),
]
