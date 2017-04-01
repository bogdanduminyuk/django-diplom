from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'wordpress_adaptation/$', views.wordpress_adaptation, name='wordpress_adaptation'),
    url(r'joomla_adaptation/$', views.joomla_adaptation, name='joomla_adaptation'),

    url(r'wordpress_adaptation/test/$', views.wp_test, name='wp_test'),
    url(r'joomla_adaptation/test/$', views.joomla_test, name='joomla_test'),
]

