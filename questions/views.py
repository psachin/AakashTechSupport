# Create your views here.

from django.template import RequestContext
from django.shortcuts import render_to_response, render, get_object_or_404
from aakashuser.models import Post, Reply
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Count
from django.contrib.auth.decorators import login_required


def all_questions_view(request, url):
    context = RequestContext(request)
    context_dict = {}

    if url == 'latest':
        posts = Post.objects.all().order_by("-post_date")
        context_dict = {
            'posts': posts,
        }

    elif url == 'frequent':
        pass

    elif url == 'active':
        pass

    elif url == 'unanswered':
        posts = Post.objects.all()
        replies = Reply.objects.all()
        files = []

        for p in posts:
            a = 0
            for r in replies:
                if r.title.title == p.title:
                    a = 1
            if a == 0:
                files.append(p)
            context_dict = {
                'posts': files,
            }

    elif url == '':
        posts = Post.objects.all()
        context_dict = {
            'posts': posts,
        }

    return render_to_response('questions/all_questions.html', context_dict, context)