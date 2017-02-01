from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'wordpress_adaptation/$', views.wordpress_adaptation, name='wordpress_adaptation'),
    url(r'joomla_adaptation/$', views.joomla_adaptation, name='joomla_adaptation'),

    url(r'test/$', views.test, name='test'),
]

