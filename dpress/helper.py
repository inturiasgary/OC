#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import datetime
import time

from django.http import Http404

def archive_month_filter(year, month, queryset, date_field):
    try:
        tt = time.strptime("%s-%s" % (year, month), '%s-%s' % ('%Y', '%m'))
        date = datetime.date(*tt[:3])
    except ValueError:
        raise Http404

    first_day = date.replace(day=1)
    if first_day.month == 12:
        last_day = first_day.replace(year=first_day.year + 1, month=1)
    else:
        last_day = first_day.replace(month=first_day.month + 1)
    lookup_kwargs = {
        '%s__gte' % date_field: first_day,
        '%s__lt' % date_field: last_day,
    }
    return queryset.filter(**lookup_kwargs), {'archive_month': date}
