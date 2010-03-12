from django.template import Library, Node, NodeList, VariableDoesNotExist, resolve_variable, TemplateSyntaxError
from django.core.paginator import *

register = Library()

class NeedPaginationNode(Node):

    def __init__(self, request, pagination, get_param_name, nodelist_true, nodelist_false):
        self.request, self.pagination, self.get_param_name = request, pagination, get_param_name
        self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false

    def __repr__(self):
        return "<NeedPaginationNode>"

    def render(self, context):

        try:
            request = resolve_variable(self.request, context)
        except VariableDoesNotExist:
            request = None
        try:
            pagination = resolve_variable(self.pagination, context)
        except VariableDoesNotExist:
            pagination = None

        try:
            get_param_name = resolve_variable(self.get_param_name, context)
        except VariableDoesNotExist:
            get_param_name = None

        if(request.GET.has_key(get_param_name)):
            current_page = int(request.GET[get_param_name])
        else:
            current_page = 0;
        has_previous = pagination.has_previous(current_page)
        has_next = pagination.has_next(current_page)
        need_pagination = has_previous or has_next

        if need_pagination:
            return self.nodelist_true.render(context)
        return self.nodelist_false.render(context)

def do_need_pagination(parser, token):
    bits = list(token.split_contents())
    if len(bits) != 4:
        raise TemplateSyntaxError, "%r takes three arguments" % bits[0]
    end_tag = 'end' + bits[0]
    nodelist_true = parser.parse(('else', end_tag))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse((end_tag,))
        parser.delete_first_token()
    else:
        nodelist_false = NodeList()
    return NeedPaginationNode(bits[1], bits[2], bits[3], nodelist_true, nodelist_false)
do_need_pagination = register.tag("needpagination", do_need_pagination)

@register.inclusion_tag('shared/pagination_top.html')
def show_pagination_top(pagination, total_items, request, get_param_name):

    if(request.GET.has_key(get_param_name)):
        current_page = int(request.GET[get_param_name])
    else:
        current_page = 1;
    page = pagination.page(current_page)
    has_previous = page.has_previous()
    has_next = page.has_next()
    need_pagination = has_previous or has_next

    num_per_page = pagination.per_page

    item_from = ((current_page-1)*num_per_page)+1

    if total_items == 0:
        item_from = 0

    item_to = total_items
    has_next = page.has_next()
    if has_next:
        item_to = current_page*num_per_page

    return locals()

@register.inclusion_tag('shared/pagination_bottom.html')
def show_pagination(pagination, request, get_param_name, ajax_class=False):

    if(request.GET.has_key(get_param_name)):
        current_page = int(request.GET[get_param_name])
    else:
        current_page = 1

    if current_page > pagination.num_pages:
        current_page = pagination.num_pages
    if ajax_class:
        pagination_class = ajax_class

    page = pagination.page(current_page)
    has_previous = page.has_previous()
    has_prev_num = page.previous_page_number()
    if has_prev_num == current_page-2:
        has_previous_previous = True
    else:
        has_previous_previous = False        
    has_next = page.has_next()

    has_next_num = page.next_page_number()
    if has_next_num == current_page+2:
        has_next_next = True
    else:
        has_next_next = False        
    need_pagination = has_previous or has_next

    has_start_page = current_page > 2
    has_end_page = (pagination.num_pages - current_page) > 3

    has_start_hellip = current_page > 3
    has_end_hellip = (pagination.num_pages - current_page) > 4

    total_pages = pagination.num_pages
    pages = pagination.page_range
    is_paginated = pagination.count > pagination.per_page,
    
    from django.utils.html import escape   
    get_params = ''
    for key, value in request.GET.iteritems():        
        if not key == get_param_name:            
            if get_params == '':
                get_params = '?'+key+'='+escape(str(value))
            else:
                get_params += '&amp;'+key+'='+escape(str(value))
    if get_params == '':
        get_params = '?'+get_param_name+'='
    else:
        get_params += '&amp;'+get_param_name+'='

    return locals()
