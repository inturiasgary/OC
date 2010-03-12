from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import Count
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from datetime import date, timedelta, datetime
import calendar
import itertools

class DefaultRrManager(models.Manager):
    def get_query_set(self):
        return super(DefaultRrManager, self).get_query_set()


class EventPublishedManager(models.Manager):

    def get_query_set(self):
        return super(EventPublishedManager, self).get_query_set().filter(published=True)

    def events_on_year(self, year=date.today().year, limit=None):
        last_day_on_month   = get_last_day_on_month(year, 12)
        qs                  = self.get_query_set().filter(start_date__lte=datetime(year=year, month=12, day=last_day_on_month, hour=23, minute=59, second=59), end_date__gte=datetime(year=year, month=1, day=1)).order_by('start_date')
        if limit:
            return qs[:limit]
        else:
            return qs

    def events_on_month(self, year=date.today().year, month=date.today().month, limit=None):
        last_day_on_month   = get_last_day_on_month(year, month)
        qs                  = self.get_query_set().filter(start_date__lte=datetime(year=year, month=month, day=last_day_on_month, hour=23, minute=59, second=59), end_date__gte=datetime(year=year, month=month, day=1)).order_by('start_date')
        if limit:
            return qs[:limit]
        else:
            return qs

    def events_on_day(self, year=date.today().year, month=date.today().month, day=date.today().day, limit=None):
        qs = self.get_query_set().filter(start_date__lte=datetime(year=year, month=month, day=day, hour=23, minute=59, second=59), end_date__gte=datetime(year=year, month=month, day=day)).order_by('start_date')
        if limit:
            return qs[:limit]
        else:
            return qs

    def events_upcoming(self, limit=None):
        qs = self.get_query_set().filter(start_date__gte=datetime(year=datetime.today().year, month=datetime.today().month, day=datetime.today().day)).order_by('start_date')
        if limit:
            return qs[:limit]
        else:
            return qs

    def get_calendario(self):
        return self.calendario

    def calendar(self, year=date.today().year, month=date.today().month):
        c                   = calendar.Calendar(calendar.SUNDAY)
        self.myCal          = c.monthdayscalendar(year, month)
        auxCal              = c.monthdayscalendar(year, month)
        last_week           = auxCal.pop()
        last_week.sort(reverse=True)
        last_day_on_month   = last_week[0]
        events              = Event.publishedM.filter(end_date__gte=date(year, month,1), start_date__lte=date(year, month, last_day_on_month))
        fields = []
        for week in self.myCal:
            for day in week:
                fields.append(day)
        self.calendario=dict(map(lambda k: (k,[]), fields))
        for event in events:
            self.init_date  = event.start_date.date()
            end_date        = event.end_date.date()
            days            = (end_date - self.init_date).days
            dates           = list(itertools.islice(date_generator(self),days+1))
            for week in self.myCal:
                for day in week:
                    if day!=0:
                        if '%s,%s,%s'%(year, month, day) in dates:
                            self.calendario[day].append(event)
        return self.calendario

    def eventInDate(self, day):
        return self.calendario[day]

    def eventCountInDate(self, day):
        try:
            return self.eventInDate(day).__len__()
        except:
            return 0


def date_generator(self):
    from_date  = self.init_date
    while True:
        yield ('%s,%s,%s')%(from_date.year, from_date.month, from_date.day)
        from_date = from_date + timedelta(1)

def get_last_day_on_month(year=date.today().year, month=date.today().month):
    c                   = calendar.Calendar()
    auxCal              = c.monthdayscalendar(year, month)
    last_week           = auxCal.pop()
    last_week.sort(reverse=True)
    return last_week[0]

class Event(models.Model):
    '''
    >>from datetime import datedef get_calendario(self):
        return self.calendario
    >>from opendoor.apps.events.models import *
    >>Event.objects.all()
    >>Event.published.all()
    >>Event.upcoming.all()
    >>Event.objects.EventInRange(date(2001,1,1),date(2010,1,1))
    >>event1 = Event.objects.create(event_date=date(2009,11,26), title="test title now", excerpt="test excerpt", description="test description", published=True, publish_on=date(2009, 11,25))
    '''
    user        = models.ForeignKey(User)
    start_date  = models.DateTimeField(_('* Start Date'))
    end_date    = models.DateTimeField(_('* End Date'))
    title       = models.CharField(_('* Title'),max_length=100)
    excerpt     = models.CharField(_('* Excerpt'),max_length=100)
    description = models.TextField(_('Description'),max_length=100, blank = True)
    location    = models.CharField(_('Location'), max_length=100, blank = True)
    published   = models.BooleanField(_('Is Publish?'), default = False)
    publish_on  = models.DateField(_('Publish On'), null = True)
    icon        = models.ImageField(_('Icon'), upload_to='icon/', blank = True)
    registered  = models.DateField(_('Registered'), auto_now_add = True)
    objects     = DefaultRrManager()
    publishedM  = EventPublishedManager()

    def __unicode__(self):
        return self.title

    class Meta:
        ordering        = ['-start_date']
        get_latest_by   = '-start_date'

    def check_published(self):
        if self.publish_on == date.today():
            self.published = True

    @models.permalink
    def get_absolute_url(self):
        return('event_detail',(),{'event_id':self.id})

    def save(self, instance=None, **kwargs):
        ''' generate raise exception '''
	if instance is None:
	        if (self.start_date >= datetime.today() and self.end_date >= self.start_date and self.publish_on <= self.start_date.date()):
        		return super(Event, self).save(**kwargs)
     	else:
		if (self.end_date >= self.start_date and self.publish_on <= self.end_date.date()):
			return super(Event, self).save(**kwargs)
