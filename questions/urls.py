__author__ = 'shubham'

from django.conf.urls import patterns, include, url
from questions import views

urlpatterns = patterns(
    '',
    #url(r'^$', views.main, name='main'),

    url(r'^()$', views.all_questions_view, name='question'),
    url(r'^tag/$', views.tag, name='tag'),
    url(r'^tag_search/$', views.tag_search, name='tag_search'),


)