# -*- coding: utf-8 -*-
from django import template
from django.conf import settings
from myproject.events.models import *
from datetime import date, timedelta

#from django.template import Context, loader, RequestContext
from myproject.utils.tools import paginate_objects, auto_render
#from django.http import HttpResponseRedirect
from django.conf import settings

register = template.Library()

@auto_render
@register.inclusion_tag('events/events_for_month.html')
def event_for_month(year, month, request):
    events_month = Event.publishedM.events_on_month(year, month)
    c = {}
    #c['total_events'] = events_month.count()

    c.update(paginate_objects(request, events_month, 'events_month', settings.EVENTS_MONTH_IN_LIST, 'ev_m'))

    return c


@register.inclusion_tag('events/events_for_day.html')
def events_for_day( year, month, day ):
    events_on_day = Event.publishedM.events_on_day(year, month, day)
    return{
	   'events_on_day': events_on_day,
	  }

@register.inclusion_tag('events/get_upcomming_events.html')
def get_upcomming_events(num_e):
    upcomming_events = Event.publishedM.events_upcoming(num_e)
    return{
	   'upcomming_events': upcomming_events,
	  }


def get_latest_events(parser, token):
    """
        {% get_latest_events 5 as events_items %}
    """
    bits = token.split_contents()
    if len(bits) == 3:
        limit = None
    elif len(bits) == 4:
        try:
            limit = abs(int(bits[1]))
        except ValueError:
            raise template.TemplateSyntaxError("If provided, second argument to `get_latest_events` must be a positive whole number.")
    if bits[-2].lower() != 'as':
        raise template.TemplateSyntaxError("Missing 'as' from 'get_latest_events' template tag.  Format is {% get_latest_events 5 as events_items %}.")
    return LatestEventsItemNode(bits[-1], limit)

class UpComingEventsNode(template.Node):
    def __init__(self, limit=1, varname="events"):
        self.limit=limit
        self.varname = varname

    def render(self, context):
        try:
            context[self.varname] = Event.publishedM.events_upcoming(self.limit)
        except:
            context[self.varname] = []
        return u''

def upcoming_events(parser, token):
    """
        {% get_upcoming_events 2 as events %}
    """
    bits = token.split_contents()
    return UpComingEventsNode(bits[1], bits[-1])

class LatestEventsItemNode(template.Node):
    """
    Returns a QuerySet of published Event
    """

    def __init__(self, varname, limit=None):
        self.varname = varname
        self.limit = limit

    def render(self, context):
        #TODO: filter latest events
        events = Event.publishedM.filter()

        # Apply a limit.
        if self.limit:
            events = events[:self.limit]

        context[self.varname] = events
        return u''

register.tag(get_latest_events)
register.tag(upcoming_events)
