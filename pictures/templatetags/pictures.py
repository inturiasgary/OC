# -*- coding: utf-8 -*-
"""Picture template tags"""
from django import template
from django.template import Template, TemplateSyntaxError

register = template.Library()

class GetGalleryNode(template.Node):
    """Load picture node."""
    def __init__(self, varname):
        self.varname = varname

    def render(self, context):
        if 'current_page' in context:
            current_page = context['current_page']
            if current_page != None:
                try:
                    gallerypage = current_page.gallerypage_set.all()[0]
                    context[self.varname] = gallerypage.gallery.pictures.all()
                    context['pictures_count']=range(1,gallerypage.gallery.pictures.count()+1)
                except:
                    context[self.varname] = None
                    context['pictures_count'] = [0]
        return ''

def do_get_gallery(parser, token):
    """ Store the gallery of the page in the context

    Example::

        {% get_gallery as varname %}

    """
    bits = token.split_contents()
    if 4 <= len(bits) <= 2:
        raise TemplateSyntaxError('%r expects 3 arguments' % bits[0])
    if bits[-2] != 'as':
        raise TemplateSyntaxError('%r expects "as" as the second last argument' % bits[0])
    varname = bits[-1]
    return GetGalleryNode(varname)
do_get_gallery = register.tag('get_gallery', do_get_gallery)
