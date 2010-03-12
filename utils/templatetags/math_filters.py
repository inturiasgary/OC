from django.template import Library

register = Library()

def sub(value, arg=None):
    return value-arg

register.filter('sub', sub)
