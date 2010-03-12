from django.conf.urls.defaults import *
import views
from feeds import LatestDPressPostFeed

feeds = {
    'latest': LatestDPressPostFeed,
}

urlpatterns = patterns('',
    # Example:
    url(r'^$', views.index, name='dpress_index'),
    url(r'^a/(?P<year>\d{4})/(?P<month>\d{1,2})/$', views.index, name='dpress_month_archive'),
    url(r'^tags/(?P<tag>[-\w]+)/$', views.index, name='dpress_tag'),
    url(r'^post/(?P<username>[-\w]+)/(?P<year>\d{4})/(?P<month>\d{2})/(?P<slug>[-\w]+)/$', 
        views.post, name='dpress_post'),
    url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed',
        {'feed_dict': feeds}, name='dpress_feeds'),

)

from django.views.generic.simple import direct_to_template

urlpatterns += patterns('',
    # Example:
    (r'^test/base/$', direct_to_template, {'template': 'dpress/base.html'}),
    (r'^test/ext_base/$', direct_to_template, {'template': 'dpress/ext_base.html'}),
    (r'^test/$', direct_to_template, {'template': 'dpress/index.html'}),
)
