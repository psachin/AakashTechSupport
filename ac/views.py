from PIL import Image as PImage
from aakashuser.models import *
from django.contrib.admin.views.decorators import staff_member_required
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Count
from ac.forms import SubmitTicketForm
import json
from django.shortcuts import render
from django import forms
from django.db.models import Max
from ac.forms import SubmitTicketForm
from django.template import RequestContext
import datetime
from django.db.models import Max
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.contrib.auth.decorators import user_passes_test
from datetime import timedelta
import re
from django.contrib import messages
from django.core.mail import send_mail
def special_match(strg, search=re.compile(r'[^a-z0-9.]').search):
     return not bool(search(strg))
@login_required
def submit_ticket(request):
    if request.method == "POST":
        if request.user.email != request.POST["user_id"]:
	    #checking whether the email id submitted by the user is the same as the email id he registered with
            return render_to_response('ac/email_not_valid.html', {"message": "Please enter a valid email id; the email id you used during registration!"}, RequestContext(request))
        if request.user.is_authenticated() and request.user.email == request.POST["user_id"]:
	    user_tab_id = request.POST["tab_id"]
	    if len(user_tab_id) != 8 and not special_match(user_tab_id):
                return render_to_response('ac/email_not_valid.html', {"message": "the tablet id you entered is not valid.Please enter a valid tablet id"}, RequestContext(request))
            user_details = request.user.email
            submit_ticket_form = SubmitTicketForm(
                request.POST, user_details=user_details)#instantiating the SubmitTicketForm; passing the POST request and users email as a parameter
            print request.POST["topic_id"]
            category = Category.objects.get(category=str(request.POST["topic_id"]))#getting the category object from the Category table corresponding to the category selected from the drop down by the user
            cat_id = category.id
            submit_ticket_form.topic_id = cat_id	
            if submit_ticket_form.is_valid():
                t=datetime.datetime.now()
		t=t.strftime('%Y-%m-%d %H:%M:%S')
		Enddate = Date + datetime.timedelta(days=1)
		Invaliddate = Date - datetime.timedelta(days=1)
		ticket=Ticket.objects.get_or_create(user_id=request.POST["user_id"],
					    topic_id=category,
					    tab_id=request.POST["tab_id"],
					    message=request.POST["message"],
					    created_date_time=t,
					    overdue_date_time=Enddate,
					    closed_date_time=Invaliddate,
					    reopened_date_time=Invaliddate,
					    status=0,
					    topic_priority=1,
					    duration_for_reply=24)[0]
                print "success"
		subject="AakashTechSupport: Your ticket id is:"+str(ticket.ticket_id)
		message=request.user.email+''',

A request for support has been created and assigned ticket #'''+str(ticket.ticket_id)+'''. A representative will follow-up with you as soon as possible.

You can view this ticket's progress online by logging into your account and clicking on view tickets.'''
		my_email="aakashkumariitb@gmail.com"#CHANGE THIS WHILE DEPLOYING
		receiptents=[request.user.email]
		send_mail(subject, message, my_email, receiptents,fail_silently=False)
                return render_to_response(
                    'ac/after_submit.html',
                    {'ticket_id': ticket.ticket_id},
                    RequestContext(request)) #passing the ticket_id as a dictionary element to the template ac/after_submit.html where its displayed to the user
            else:
		#this handles the ValidationError raised in forms.py if the user enters a tablet id that is not present in the Tablet_info table
                return render_to_response('ac/email_not_valid.html', {"message": "the tablet id you entered is not valid.Please enter a valid tablet id"}, RequestContext(request))
        else:
	    #the user has to login to post and is displayed the login to post message if he does so without logging in
            return HttpResponse("login to post")
    # displaying the form for the first time. i think instance variable should
    # be passed here.
    else:
        user_details = request.user.email #get the users email
        submit_ticket_form = SubmitTicketForm(user_details=user_details) #instantiate the form
    return render_to_response(
        'ac/submit_ticket.html',
        {'submit_ticket_form': submit_ticket_form, 'user': request.user},
        RequestContext(request))

# MAIN function to display the  all the submitted 
@user_passes_test(lambda u:u.is_staff, login_url='/login/')
def main(request):
    """Main listing."""
    tickets = Ticket.objects.all()
    return render_to_response("ac/d.html", dict(tickets=tickets), RequestContext(request))

# To show all the details of a particular ticket
@user_passes_test(lambda u:u.is_staff, login_url='/login/')
def display(request, id):
    """Displaying the details of the corresponding tickets"""
    threads = Ticket.objects.get(pk=id)
    response = Threads.objects.filter(ticketreply=id)
    count = Threads.objects.filter(ticketreply=id).count()
    count_open = Ticket.objects.filter(status=0).count()
    count_close = Ticket.objects.filter(status=1).count()

    if response.exists():
        context_dict = {
            'threads': threads,
            'response': response,
            'count': count,
            'count_open': count_open,
            'count_close': count_close,
        }
    else:
        context_dict = {
            'threads': threads,
            'count_open': count_open,
            'count_close': count_close,
        }

    return render_to_response("ac/second.html", context_dict, RequestContext(request))

#Function for searching tickets
@user_passes_test(lambda u:u.is_staff, login_url='/login/')
def search(request):
    if request.method == "POST":
        Search = request.POST.get('search')
        active_user = request.user
        context_dict = {}

        """Searching for ticket-id"""
        tickets = Ticket.objects.filter(Q(ticket_id__icontains=Search) | Q(user_id__icontains=Search))

        if tickets.exists():
            context_dict = {
                'user': active_user,
                'tickets': tickets,
            }
            return render_to_response("ac/search.html", context_dict, RequestContext(request))
        else:
            """Searching for Topic-id"""
            tickets = Category.objects.filter(category__icontains=Search)

            if tickets.exists():
                tickets = Ticket.objects.filter(topic_id=tickets)
                context_dict = {
                    'user': active_user,
                    'tickets': tickets,
                }
                return render_to_response("ac/search.html", context_dict, RequestContext(request))
            else:
                tickets = Ticket.objects.all()
                context_dict = {
                    'user': active_user,
                    'tickets': tickets,
                }
                return render_to_response("ac/d.html", context_dict, RequestContext(request))


@user_passes_test(lambda u:u.is_staff, login_url='/login/')
def graph(request):
    data = {}
    category_names = []
    category = Category.objects.all()#category stores a list of all the categories
    for c in category:
	#iterating ecah category
        category_names.append(c.category)#append each category name to the category_names list
    count = {}#count will store a count of the number of tickets submitted for each category
    category = Category.objects.all()
    ticket = Ticket.objects.all()#ticket stores a list of all the tickets
    for c in category:
	#iterating over each category
        count[c.category] = 0#initializing the count of each category as 0
        for t in ticket:
	    #iterating over all the tickets	
<<<<<<< HEAD
	    ticket_for_a_cat=[]	
            ticket_for_a_cat = Ticket.objects.filter(topic_id=c)#ticket_for_a_cat is a list that contains tickets corresponding to the category	
=======
            ticket_for_a_cat = Ticket.objects.filter(topic_id=c)#ticket_for_a_cat is a list that contains tickets corresponding to the category c
>>>>>>> upstream/master
            count[c.category] = ticket_for_a_cat.count()#updating the count of each category as the number of elements in ticket_for_a_cat list
    return render_to_response("ac/graphs.html", {'count': count, 'category_names': category_names}, RequestContext(request))#passing the count and category_names dictionary to graphs.html template for rendering graph


@user_passes_test(lambda u:u.is_staff, login_url='/login/')
def ticket_status_graph(request):
    tickets = Ticket.objects.all()#ticket stores a list of all the tickets
    t_open = 0#intializing the open ticket count as 0
    t_closed = 0#intializing the open ticket count as 1
    for t in tickets:
	#iterating over all the tickets
        status = t.status#get the status of the ticket t
        if status == 0:
            t_open = t_open + 1#increment t_open if status is 0 i.e open
        if status == 1:
            t_closed = t_closed + 1#increment t_closed if status is 1 i.e closed
    status_dict = {'open': t_open, 'closed': t_closed}#stores the number of open and closed tickets
    return render_to_response("ac/graphs_tickets.html", {'status_dict': status_dict}, RequestContext(request))#passing the status_dict dictionary to graphs_tickets.html template for rendering graph of open vs closed tickets


@user_passes_test(lambda u:u.is_staff, login_url='/login/')
def ticket_traffic_graph(request):
    from datetime import date	
    year = date.today().year#get the current year
    ticket_dict = {}
    for i in range(1, 13):
	#i represents each month of the year
        tickets_in_i = Ticket.objects.filter(created_date_time__year=year,
                                             created_date_time__month=i)#filter tickets having the created year equal to year and created month equal to i
        tickets_in_i_count = tickets_in_i.count()#count the number of tickets in the month i
        ticket_dict[i] = tickets_in_i_count#update the dictionary to include the value of the number of tickets in the month i
    return render_to_response("ac/ticket_traffic.html", {'ticket_dict': ticket_dict}, RequestContext(request))#passing the ticket_dict dictionary to ticket_traffic.html template for rendering graph of ticket traffic

#To post the ADMIN REPLY
@user_passes_test(lambda u:u.is_staff, login_url='/login/')
def reply(request, id):
    if request.method == 'POST':
        Reply = request.POST.get('response')
        ticket = Ticket.objects.get(pk=id)

        response = Threads.objects.create(
            ticketreply=ticket, reply=Reply, count=1)
        response.save()
	subject="AakashTechSupport: Response to your ticket id #"+str(id)
	message=ticket.user_id+''',
A customer support staff member has replied to your support request, #'''+id+''' with the following response:

'''+Reply+'''

We hope this response has sufficiently answered your questions.If so please login to your account and close the ticket. Login to your account for a complete archive of all your support requests and responses.'''
	my_email="aakashkumariitb@gmail.com"#CHANGE THIS WHILE DEPLOYING
	receiptents=[ticket.user_id]
	send_mail(subject, message, my_email, receiptents,fail_silently=False)
        check = request.POST.get('reply_ticket_status')
        print check
        if check == 'Open':
            s = Ticket.objects.get(pk=id)
            s.status = 0
            s.save()

        threads = Ticket.objects.get(pk=id)
        response = Threads.objects.filter(ticketreply=id)
        count = Threads.objects.filter(ticketreply=id).count()
        count_open = Ticket.objects.filter(status=0).count()
        count_close = Ticket.objects.filter(status=1).count()

        context_dict = {
            'threads': threads,
            'response': response,
            'count':  count,
            'count_open': count_open,
            'count_close': count_close,
        }

        return render_to_response("ac/second.html", context_dict, RequestContext(request))


@user_passes_test(lambda u:u.is_staff, login_url='/login/')
def open(request):
    tickets = Ticket.objects.filter(status=0)
    return render_to_response("ac/d.html", dict(tickets=tickets), RequestContext(request))


@user_passes_test(lambda u:u.is_staff, login_url='/login/')
def close(request):
    tickets = Ticket.objects.filter(status=1)
    return render_to_response("ac/d.html", dict(tickets=tickets), RequestContext(request))


@login_required
def view_tickets(request):
    #this view enables the user to view all the tickets submitted by him
    email = request.user.email#the the users email
    tickets = Ticket.objects.filter(user_id=email)#get all the tickets submitted by the user
    if not tickets:
	#if user has submitted no tickets so far redirect him to a page showing the message No tickets to display
        return render_to_response("ac/email_not_valid.html", {"message": "No tickets to display"}, context_instance=RequestContext(request))
    else:
	#display the users tickets
        tickets_dict = []#this list will contain all the ticket details
        for t in tickets:
            t_dic = {}#stores details of each ticket
	    #setting the content of the dictionary as the data of each ticket	
            if t.status == 0:
                status = "open"
            if t.status == 1:
                status = "closed"
            t_dic["status"] = status
            t_dic["tablet id"] = t.tab_id
            t_dic["message"] = t.message
            t_dic["created date and time"] = t.created_date_time
            t_dic["ticket id"] = t.ticket_id
            if t.topic_priority == 0:
                p = "low"
            if t.topic_priority == 1:
                p = "normal"
            if t.topic_priority == 2:
                p = "high"
            t_dic["priority"] = p
            replies = Threads.objects.filter(ticketreply=t.ticket_id)#get all the replies corresponding to a given ticket
            if not replies:
                reply_str = "No replies yet"#if there are no replies
            else:
                reply_str = ""
            for reply in replies:
                reply_str = reply_str + "Reply on " + \
                    reply.created.strftime(
                        '%Y-%m-%d') + " : " + reply.reply + " ;"#concatenated each reply by the admin along with the date of the reply to the reply_str string
            t_dic["Replies"] = reply_str
            tickets_dict.append(t_dic)#append the t_dic dictionary to the tickets_dict list
        return render_to_response("ac/view_tickets.html", {"tickets_dict": tickets_dict}, context_instance=RequestContext(request))#passing the tickets_dict dictionary to view_tickets.html template for displaying ticket details


@login_required
def close_ticket(request, id):
	"""closing a ticket"""
	logged_in_user_email=request.user.email
	ticket=Ticket.objects.filter(ticket_id=id)
	print ticket
	if not ticket:
		return render_to_response('ac/email_not_valid.html', {"message": "No such ticket exists!"}, RequestContext(request))
	else:
		ticket=ticket[0]
		ticket_submitter_user_email=ticket.user_id
		if logged_in_user_email==ticket_submitter_user_email:
			if ticket.status==0:#ticket is open
				ticket.status=1
				now=datetime.datetime.now()
				print now
				ticket.closed_date_time=now.strftime('%Y-%m-%d %H:%M:%S')
				ticket.save()
			else:
				return render_to_response('ac/email_not_valid.html', {"message": "You have already closed this ticket!"}, RequestContext(request))			
		else:
			return render_to_response('ac/email_not_valid.html', {"message": "you can close tickets submitted only by you!"}, RequestContext(request))
	return render_to_response('ac/email_not_valid.html', {"message": "The ticket has been closed! Happy that your problem was resolved!"}, RequestContext(request))


@user_passes_test(lambda u:u.is_staff, login_url='/login/')
def make_csv(request):
	'''
	dumps all the data from the ticket table into the ticket_data.csv file
	'''
	#file_obj=open("data_of_rc.csv")
	#print file_obj
	#file_obj.close()
	import csv
	response = HttpResponse(mimetype='text/csv')
	response['Content-Disposition'] =  'attachment; filename=ticket_data.csv'
	writer = csv.writer(response)
	#writer = csv.writer(open("ticket_data.csv", 'w'))	
	headers = []
	for field in Ticket._meta.fields:
		headers.append(field.name)
	writer.writerow(headers)
	ticket=Ticket.objects.all()
	for t in ticket:
	  row=[]
	  user_id=t.user_id
	  topic_id=t.topic_id
	  tab_id=t.tab_id
	  message=t.message
	  ticket_id = t.ticket_id
	  created_date_time=t.created_date_time.strftime("%d/%m/%Y %H:%M:%S")
	  overdue_date_time=t.overdue_date_time.strftime("%d/%m/%Y %H:%M:%S")
	  closed_date_time=t.closed_date_time.strftime("%d/%m/%Y %H:%M:%S")
	  status=t.status
	  reopened_date_time=t.reopened_date_time.strftime("%d/%m/%Y %H:%M:%S")
	  topic_priority=t.topic_priority
	  duration_for_reply=t.duration_for_reply
	  row.append(user_id)
	  row.append(topic_id)
	  row.append(tab_id)
	  row.append(message)
	  row.append(ticket_id)
	  row.append(created_date_time)
	  row.append(overdue_date_time)
	  row.append(closed_date_time)
	  row.append(status)
	  row.append(reopened_date_time)
	  row.append(topic_priority)
	  row.append(duration_for_reply)
	  #print row
	  writer.writerow(row)
	return response

