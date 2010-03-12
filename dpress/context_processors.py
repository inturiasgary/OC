#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.conf import settings

def common(request):
    """
    Adds media-related context variables to the context.

    """
    return {'BLOG_CONFIG': settings.BLOG_CONFIG, 'PREFIX_URL': settings.PREFIX_URL}
