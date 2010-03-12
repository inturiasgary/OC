from django.conf.urls.defaults import *

urlpatterns = patterns('links.views',
    url(r'^$', 'links_list'),
    url(r'^categories/$', 'categories_list', name='categories_list'),
    url(r'^categories/(?P<category_slug>\S+)/$', 'links_by_category', name='links_by_category'),
)
