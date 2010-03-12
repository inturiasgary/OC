from django import template
from django.conf import settings
from myproject.links.models import Category, Link

register = template.Library()

@register.inclusion_tag('links/links.html')
def links_for_category(category):
    try:
        cat = Category.objects.get(slug=category)
        links = cat.link_categories.all()
    except Category.DoesNotExist:
        pass

    return{
	   'links': links ,
	  }

@register.inclusion_tag('links/links.html')
def links_list():
    links = Link.objects.all()

    return{
        'links': links ,
    }

@register.inclusion_tag('links/categories.html')
def categories_list():
    categories = Category.objects.all()

    return{
        'categories': categories ,
    }
