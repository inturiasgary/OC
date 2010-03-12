#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.template.context import RequestContext
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from django.views.generic.list_detail import object_list
from django.contrib import comments

from tagging.models import Tag, TaggedItem

from models import Post
from helper import archive_month_filter

def index(request, username=None, tag=None, year=None, month=None,
        template_name="dpress/index.html"):
    extra_context = {}
    if tag:
        tag = get_object_or_404(Tag, name=tag)
        extra_context['tag'] = tag
        posts = TaggedItem.objects.get_by_model(Post, tag)
    else:
        posts = Post.objects.all()
    posts = posts.filter(status=2).select_related(depth=1)
    if year and month:
        posts, t_context = archive_month_filter(year, month, posts, 'publish')
        extra_context.update(t_context)
    posts = posts.order_by("-publish")
        
    if username is not None:
        user = get_object_or_404(User, username=username.lower())
        posts = posts.filter(author=user)
    return object_list(request,
                       posts,
                       paginate_by=5,
                       template_name=template_name,
                       extra_context=extra_context,
                       allow_empty=True)        

def post(request, username, year, month, slug,
         template_name="dpress/post.html"):
    post = Post.objects.filter(slug=slug, publish__year=int(year), 
            publish__month=int(month)).filter(author__username=username)
    if not post:
        raise Http404
    if post[0].status == 1 and post[0].author != request.user:
        raise Http404
    post=post[0]
    user = request.user
    initial={}
    if user.is_authenticated():
        initial={'name': user.username, 'email': user.email}
    form = comments.get_form()(post, initial=initial)
    if request.method == "POST":
        data = request.POST.copy()
        form = comments.get_form()(post, data=data)
        if form.is_valid():
            comment = form.get_comment_object()
            comment.ip_address = request.META.get("REMOTE_ADDR", None)
            if request.user.is_authenticated():
                comment.user = request.user
            comment.save()
    return render_to_response(template_name, {
        "post": post,
        "form": form,
    }, context_instance=RequestContext(request))
