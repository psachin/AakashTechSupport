from django.conf.urls  import patterns , include , url


urlpatterns = patterns( '',
             
     url(r'^$', 'ticketing.views.main', name='Main'),
     url(r'^back', 'ticketing.views.main'),
     url(r'^display/(\d+)/$', "ticketing.views.display"),
     url(r'^search/$', "ticketing.views.search"),
     url(r'^graphs', "ticketing.views.graph"),
     url(r'^reply/(\d+)/(\d+)/$', "ticketing.views.reply"),
     url(r'^submit_ticket/', 'ticketing.views.submit_ticket', name='submit ticket'),
     url(r'^ticket_stats/', 'ticketing.views.ticket_status_graph', name='ticket stats'),
     url(r'^ticket_traffic/', 'ticketing.views.ticket_traffic_graph', name='ticket traffic'),
     url(r'^open/', 'ticketing.views.open', name='open'),
     url(r'^close/', 'ticketing.views.close', name='close'),
     url(r'^view_tickets/', 'ticketing.views.view_tickets', name='view tickets'),
     url(r'^login/$', include('aakashuser.urls')),
     url(r'^close_ticket/(\d+)/$', "ticketing.views.close_ticket"),
     url(r'^ticket_csv/$', "ticketing.views.make_csv"),
     url(r'^unapproved/$', 'ticketing.views.view_unapproved_ques',name='view_unapproved_ques'),
     url(r'^approve_post/(?P<id>\d+)/$', 'ticketing.views.approve_post',name='approve_post'),
     url(r'^unapproved_ans/$', 'ticketing.views.view_unapproved_ans',name='view_unapproved_ans'),
     url(r'^approve_reply/(?P<id>\d+)/$', 'ticketing.views.approve_reply',name='approve_reply'),
     url(r'^ticket_csv/$', "ticketing.views.make_csv"),
     url(r'^download_report/$',"ticketing.views.download_csv"),
		
)
