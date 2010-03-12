from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    (r'^i18n/', include('django.conf.urls.i18n')),
    (r'^pages/', include('pages.urls')),
    (r'^admin/filebrowser/', include('filebrowser.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^news/', include('news.urls')),
    (r'^events/', include('events.urls')),
    (r'^sermons/', include('sermons.urls')),
    (r'^links/', include('links.urls')),
    (r'^tinymce/', include('tinymce.urls')),
    (r'^blog/', include('dpress.urls')),
    (r'', include('pages.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        # Trick for Django to support static files
        # (security hole: only for Dev environement! remove this on Prod!!!)
        (r'', include('staticfiles.urls')),
    )
