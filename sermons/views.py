from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from sermons.models import Pastor, Subject, Sermon
from django.template import Template, RequestContext, Context
from datetime import date

def sermons_list(request, template_name='sermons/sermons_list.html'):
    sermons = Sermon.objects.all()

    return render_to_response(template_name, {"sermons":sermons}, context_instance=RequestContext(request))

def pastors_list(request, template_name='sermons/pastors_list.html'):
    pastors = Pastor.objects.all()

    return render_to_response(template_name, {"pastors":pastors}, context_instance=RequestContext(request))

def subjects_list(request, template_name='sermons/subjects_list.html'):
    subjects = Subject.objects.all()

    return render_to_response(template_name, {"subjects":subjects}, context_instance=RequestContext(request))

def sermon_by_slug(request, sermon_slug, template_name='sermons/sermon_page.html'):
    sermon = get_object_or_404(Sermon, slug=sermon_slug)

    return render_to_response(template_name, {"sermon":sermon}, context_instance=RequestContext(request))

def sermons_by_pastor(request, pastor_slug, template_name='sermons/sermons_by_pastor.html'):
    pastor = get_object_or_404(Pastor, slug=pastor_slug)
    sermons = pastor.pastor_sermons.all()

    return render_to_response(template_name, {"pastor":pastor, "sermons":sermons}, context_instance=RequestContext(request))

def sermons_by_subject(request, subject_slug, template_name='sermons/sermons_by_subject.html'):
    subject = get_object_or_404(Subject, slug=subject_slug)
    sermons = subject.subject_sermons.all()

    return render_to_response(template_name, {"subject":subject, "sermons":sermons}, context_instance=RequestContext(request))

def sermons_by_year(request, year, template_name='sermons/sermons_by_year.html'):
    sermons = Sermon.objects.filter(date__year=year)

    return render_to_response(template_name, {"year":year, "sermons":sermons}, context_instance=RequestContext(request))

def sermons_by_month(request, month, template_name='sermons/sermons_by_month.html'):
    months = {"january" : 1, "february" : 2, "march" : 3, "april" : 4, "may" : 5, "june" : 6, "july" : 7, "august" : 8,
              "september" : 9, "october" : 10, "november" : 11, "december" : 12 }
    month = month.lower()

    try:
        sermons = Sermon.objects.filter(date__month=months[month], date__year=date.today().year)
    except KeyError:
        raise Http404

    return render_to_response(template_name, {"month":month, "sermons":sermons}, context_instance=RequestContext(request))




