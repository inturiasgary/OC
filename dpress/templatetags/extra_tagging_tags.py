#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.template import Library

register = Library()

@register.inclusion_tag("dpress/include/tag_list.html")
def show_tags_for(obj):
    return {"obj": obj}
