__author__ = 'shubham'

from django.conf.urls import patterns, include, url
from questions import views

urlpatterns = patterns(
    '',
    #url(r'^$', views.main, name='main'),

    url(r'^()$', views.all_questions_view, name='question'),
    #url(r'^tag/$', views.tag, name='tag'),
    url(r'^tags/$', views.view_tags, name='tags'),
    url(r'^(unanswered)/$', views.all_questions_view, name='unans'),
    url(r'^(latest)/$', views.all_questions_view, name='latest'),
    url(r'^(frequent)/$', views.all_questions_view, name='frequent'),
    url(r'^(votes)/$', views.all_questions_view, name='votes'),
    url(r'^tags/(?P<qid>\d+)/$', views.linktag, name='linktag'),
    url(r'^(?P<qid>\d+)/$', views.link_question, name='link_question'),
    url(r'^tag_search/$', views.tag_search, name='tag_search'),

)
