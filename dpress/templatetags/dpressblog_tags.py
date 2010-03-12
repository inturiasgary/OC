#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.template import Library
from django.conf import settings

from dpress.models import Post

register = Library()

@register.inclusion_tag("dpress/include/tag_list.html")
def show_tags_for_post(obj):
    return {"obj": obj}

@register.inclusion_tag('dpress/include/content.html')
def render_content(content, markup):
    return {
        'content': content,
        'markup': markup
    }

@register.inclusion_tag('dpress/include/tease.html')
def render_tease(blog):
    return {
        'o': blog
    }
    
@register.inclusion_tag("dpress/include/last_post.html")
def last_post():
    blogs = Post.objects.filter(status=2).select_related(depth=1).order_by("-publish")
    return {
            'blogs': blogs[:5]
    }

@register.inclusion_tag("dpress/include/month_links.html")
def month_links():
    return {
            'dates': Post.objects.dates('publish', 'month')[:12],
            }

@register.inclusion_tag("dpress/include/import_syntaxhighlighter.html")
def import_syntaxhighlighter_js():
    SYNTAXHIGHLIGHTER_JS_URL = getattr(settings, 'SYNTAXHIGHLIGHTER_JS_URL', None)    
    return {'SYNTAXHIGHLIGHTER_JS_URL': SYNTAXHIGHLIGHTER_JS_URL}
