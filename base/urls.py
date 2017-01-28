from django.conf.urls import url, include
from base import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^generation/', include('generation.urls')),
    url(r'^adaptation/', include('adaptation.urls')),
]