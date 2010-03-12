from sermons.views import *
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', sermons_list),
    url(r'^pastors/$', pastors_list),
    url(r'^pastors/(?P<pastor_slug>\S+)/$', sermons_by_pastor, name='sermons_by_pastor'),
    url(r'^subjects/$', subjects_list),
    url(r'^subjects/(?P<subject_slug>\S+)/$', sermons_by_subject, name='sermons_by_subject'),
    url(r'^archive/(?P<year>\d{4})/$', sermons_by_year, name='sermons_by_year'),
    url(r'^archive/(?P<month>\S+)/$', sermons_by_month, name='sermons_by_month'),
    url(r'^(?P<sermon_slug>\S+)/$', sermon_by_slug, name='sermons_by_slug'),
)
