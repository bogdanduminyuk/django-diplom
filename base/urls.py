from django.conf.urls import url, include
from django.conf.urls.static import static

from base import views
from django.conf import settings
"""url(r'^success/$', views.success, name='success'),
    url(r'^loading/$', views.loading, name='loading'),
    """

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^generation/', include('generation.urls')),
    url(r'^adaptation/', include('adaptation.urls')),
    url(r'^help/', include('help.urls')),

    url(r'^result/$', views.result, name='result'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
