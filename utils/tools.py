from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.http import Http404


def auto_render(func):
    from django.http import HttpResponse
    def _dec(request, *args, **kwargs):
        response = func(request, *args, **kwargs)
        if isinstance(response, HttpResponse):
            return response
        (template_name, context) = response
        context['template_name'] = template_name
        from django.shortcuts import render_to_response
        from django.template import RequestContext
        res = render_to_response(template_name, context, context_instance=RequestContext(request))
        return res
    return _dec


def paginate_objects(request, objects, objects_name='opendoor', object_by_page=5, get_param_name='p_contribs'):
    
    """
    Paginate objects

    Usage::
        on model::
            from opendoor.apps.utils.tools import paginate_objects
            c = {}
            c['foos_total'] = foos.count()
            c.update(paginate_objects(request, foos, 'foos', 10, 'p_foo'))
        on template::
            {% load pagination_filters %}
            {% show_pagination_top foos_paginator foos_total request "p_foo" %}
            {% show_pagination foos_paginator request "p_foo" %}

        out::
            objects (pagined)
            objects_paginator
            objects_page
    """
    # Retrieve the right page
    objects_paginator = Paginator(objects, object_by_page)
    objects_page = 1

    if get_param_name in request.GET:
        objects_page = int(request.GET[get_param_name])
    if objects_page > objects_paginator.num_pages:
        objects_page = objects_paginator.num_pages

    try:
        objects = objects_paginator.page(objects_page)
        objects = objects.object_list
    except (EmptyPage, InvalidPage):
        objects = objects_paginator.page(objects_paginator.num_pages)
        objects = objects.object_list
        #raise http.Http404()	


    return {    objects_name: objects,
                objects_name+'_paginator':  objects_paginator,
                objects_name+'_page':       objects_page,
                'request':                  request }
