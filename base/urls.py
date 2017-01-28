from django.conf.urls import url, include

from base import views

urlpatterns = [
    url(r'', views.home, name='home'),
]