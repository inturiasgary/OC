from django.conf.urls.defaults import *
from django.conf import settings
from news.models import NewsItem
import news.views as news_views

try:
	PAGINATE = settings.NEWS_PAGINATE_BY
except:
	PAGINATE = 4

news_dict = {
	'queryset': NewsItem.on_site.published(),
	'template_object_name': 'item',
}

news_date_dict = dict(news_dict, date_field='date')

urlpatterns = patterns('django.views.generic.date_based',
	url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[-\w]+)/$', 'object_detail', news_date_dict, name="news-item"),
	url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$', 'archive_day', news_date_dict),
	url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$', 'archive_month', news_date_dict),
	url(r'^(?P<year>\d{4})/$', 'archive_year',  dict(news_date_dict, make_object_list=True)),
)

urlpatterns += patterns('django.views.generic.list_detail',
	url(r'^$', 'object_list', dict(news_dict, paginate_by=PAGINATE), name="news-index"),
)

urlpatterns += patterns('',
	url(r'^tag/(?P<tag>.+)/$',news_views.by_tag,name='news-by-tag'),
	url(r'^category/(?P<category_slug>.+)/$',news_views.by_category,name='news-by-category'),
	url(r'^categor(y|ies)/$',news_views.category_list,name='news-categories'),
	url(r'^authors/(?P<author_slug>.+)/$',news_views.by_author,name='news-by-author'),
	url(r'^authors/$',news_views.author_list,name='news-authors'),
)

