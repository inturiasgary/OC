from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from events.models import Event
from django.template import Template, RequestContext, Context
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from django.views.generic.list_detail import object_list
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string

def index(request, template_name='events/index.html'):

    year = 2009
    month = 12
    day = 7
    calendar = Event.publishedM.calendar(year,month)
    events_on_day = Event.publishedM.eventInDate(day)
    num_e = 50
    events_month = Event.publishedM.events_on_month(year, month)
    return render_to_response(template_name, locals(),
                    context_instance=RequestContext(request))



def month_index(request, year = None, month = None, template_name='events/month_index.html'):
    import calendar
    '''
    create current calendar including events detail
    '''
    now = datetime.today()
    if not year:
        year = now.year
    if not month:
        month = now.month
    year = int(year)
    month = int(month)

    try:
        cal_date = date(year, month, 1)
    except ValueError:
        raise Http404

    c=calendar.Calendar(calendar.MONDAY)

    # get all the dates that will be displayed,
    # including the tail and head of previous/next months.
    # (a list of weeks, each week is a list of 7 dates.)
    dates = c.monthdatescalendar(year, month)
    # array, ['Monday', 'Tuesday'.. 0 is Mon.
    ## daynames=calendar.day_name
    # make list, cuz I can't figure out how to use the array in the template.
    # Use the first week of the calandar, which is handy
    # because it makes sure the week starts on the weekday we want it to
    # (like Sunday)
    daynames= [ calendar.day_name[d.weekday()] for d in dates[0] ]
    dates = c.monthdayscalendar(year, month)

    # get Events from the DB that are in the specified month.
    # [0][0] = first day of first week, [-1][-1], last day of last week.
    # so start/end of the range being displaied.
    #events = Event.objects.filter(eventdate__range=(dates[0][0],dates[-1][-1]))
    calendar_events = Event.publishedM.calendar(year, month)
    # some fluf to make the page usable
    prev_month=(cal_date+relativedelta(months=-1))# .month
    next_month=(cal_date+relativedelta(months=+1))# .month

    return render_to_response(template_name, locals(),
                    context_instance=RequestContext(request))


def event_detail(request, event_id , template_name='events/detail.html'):
    try:
        event = Event.objects.get(id=event_id)
    except ValueError:
        raise Http404

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

def event_list(request, year=date.today().year, month=date.today().month):
    events = Event.publishedM.events_on_month(year, month)
    return object_list(request, events, template_object_name = 'event' )
#def event_month(request, year=None, month=None):
    #now = datetime.today()
    #if not year:
        #year = now.year
    #if not month:
        #month = now.month
    #year = int(year)
    #month = int(month)
    #events = Event.publishedM.events_on_month(year, month)
