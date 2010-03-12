from django.shortcuts import render_to_response, get_object_or_404
from links.models import Link, Category
from django.template import RequestContext

def links_list(request, template_name='links/links_list.html'):
    return render_to_response(template_name, {}, context_instance=RequestContext(request))

def categories_list(request, template_name='links/categories_list.html'):
    return render_to_response(template_name, {}, context_instance=RequestContext(request))

def links_by_category(request, category_slug):
    category = get_object_or_404(Category,slug=category_slug)
    return render_to_response('links/links_by_category.html', {'category': category,},
        context_instance=RequestContext(request))
