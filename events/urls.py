from django.conf.urls.defaults import *


try:
    PAGINATE = settings = EVENTS_PAGINATE_BY
except:
    PAGINATE = 5
urlpatterns = patterns('events.views',
    url(r'^$', 'index', name='events_index'),
    url(r'^month_index/$', 'month_index', name='month_index'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$', 'month_index'),
    url(r'^(?P<event_id>\d+)/$','event_detail', name='event_detail'),

)
