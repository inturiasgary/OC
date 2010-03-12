#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.template import Library

register = Library()

def render_paginate(context):
    if 'request' in context:
        getvars = context['request'].GET.copy()
        if 'page' in getvars:
            del getvars['page']
        if len(getvars.keys()) > 0:
            context.update({"getvars": "&%s" % getvars.urlencode()})
        return context
register.inclusion_tag('pagination/pagination.html', takes_context=True)(render_paginate)
