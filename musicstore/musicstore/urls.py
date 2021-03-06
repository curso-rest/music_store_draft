from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'core.views.api_root'),
    url(r'^bands/', include('bands.urls')),
    url(r'^albums/', include('albums.urls')),
    url(r'^songs/', include('songs.urls')),
    url(r'^tracks/', include('tracks.urls')),
    url(r'^comments/', include('comments.urls')),
    url(r'^users/', include('account.urls')),
    url(r'^purchases/', include('purchases.urls')),
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
