from django.contrib.syndication.feeds import Feed
from django.conf import settings
from django.core.urlresolvers import reverse

from models import Post

class LatestDPressPostFeed(Feed):
    title = settings.BLOG_CONFIG['title']
    description_template = 'dpress/feeds/description.html'
    description = settings.BLOG_CONFIG['blog_simple_descn']

    def items(self):
        return Post.objects.filter(status=2).order_by("-publish")[:10]

    def item_pubdate(self, item):
        return item.publish

    def link(self):
        return reverse('dpress_index')
