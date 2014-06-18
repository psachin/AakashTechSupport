# Create your views here.
import datetime
from django.db.models.signals import post_delete

__author__ = 'ushubham27'

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.context_processors import csrf
from django.core.validators import validate_email
from django.contrib.auth.models import User
from forms import UserForm
from aakashuser.models import Post, UserProfile
from taggit.models import Tag
from aakashuser.models import *
import re
# INDEX PAGE VIEW

def index(request):
    return render_to_response("index.html", request)

def search(request):
    c = {}
    c.update(csrf(request))
    return render_to_response("search.html", c)

# REGISTER VIEW

def validateEmail(email):
    if len(email) > 6:
        #if re.match('\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b', email) is not None:
        if re.match(r'\b[A-Za-z0-9._+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}\b', email) is not None:
            return 1
    return 0

def register(request):
    context = RequestContext(request)
    temp_dict = {}

    if request.POST:
        postform = UserForm(data=request.POST)

        if postform.is_valid():
            pwd = request.POST['password']
            rpwd = request.POST['password1']
            username = request.POST['username']
            email = request.POST['email']

            print username

            if pwd == rpwd and validateEmail(email):
                temp_user = postform.save(commit=True)
                new_user = User.objects.get(username=request.POST['username'])
                new_user.set_password(pwd)
                new_user.save()

                return HttpResponseRedirect('/index/')
            else:
                er1 = ""
                er2 = ""
                if not validateEmail(email):
                    er2 = "Enter a valid email address. "
                    print er2
                if pwd != rpwd:
                    er1 = "Passwords don't match."

                temp_dict = {
                    'er1': er1,
                    'er2': er2
                }

        else:
            print postform.errors
    else:
        postform = UserForm()

    context_dict = {
        'postform': postform,
    }
    context_dict.update(temp_dict)

    return render_to_response("register.html", context_dict, context)

# LOGIN VIEW

def login_x(request):
    session_id = ""
    if request.method == 'POST':
        try:
            m = User.objects.get(username=request.POST['username'])
            if m.password == request.POST['password']:
                request.session['id'] = m.email_id
                session_id = request.session['id']

                login_dict = {
                    'm': m,
                    'session_id': session_id,
                }
                return render_to_response('index.html', login_dict)
        except User.DoesNotExist:
            return HttpResponse("Your username and password pair didn't match.")
    else:
        c = {}
        c.update(csrf(request))
        context = RequestContext(request)
        return render_to_response("login.html", c, context)


def logout_x(request):
    try:
        del request.session['id']
        msg = "You have been succesfully logged out."
        print msg
    except KeyError:
        msg = "KeyError : Unable to Logout "
        print msg

    logout_msg = {
        'msg': msg
    }

    return HttpResponseRedirect('/index/', logout_msg)


def login_new(request):
   # t = loader.get_template('registration/login.html') - not needed
    context = RequestContext(request)
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                request.session['id'] = user.email
                session_id = request.session['id']
                login_error = ""
                login_dict = {
                    'user': user,
                    'session_id': session_id,
                    'login_error': login_error,
                }
		if request.user.is_superuser:
                    tickets = Ticket.objects.all()
                    return render_to_response("ac/d.html",dict(tickets=tickets), RequestContext(request))
                else:
                    response = render_to_response('index.html', login_dict)
                    return response
               
#               response.set_cookie('logged_in', user.email)
            else:
                login_error = "You are not an active user."
                login_dict = {
                    'login_error': login_error
                }
                return render_to_response('login.html', login_dict, context)
        else:
            login_error = "User authentication failed."
            login_dict = {
                'login_error': login_error
            }
            return render_to_response('login.html', login_dict, context)
    else:
        #URL was accessed directly
        c = {}
        c.update(csrf(request))
        context = RequestContext(request)
        return render_to_response('login.html', c, context)


def logout_new(request):
    logout(request)
    response = HttpResponseRedirect('/index/')
    #response.delete_cookie('logged_in')
    print "You have been logged out successfully."
    return response


def display_questions(request):
    return render_to_response('questions.html')

def ask_question(request):
    context = RequestContext(request)
    if request.POST:
        title = request.POST['post_title']
        body = request.POST['post_text']
        post_date = datetime.datetime.now()
        upvotes = 0

        u = User.objects.get(username=request.user.username)
        print "Username : "
        print u.username

        some_user = UserProfile.objects.get(user=u)

        creator_id = some_user.id
#        post.creator.id = creator_id

        print creator_id

        post = Post.objects.create(title=title, body=body, post_date=post_date, upvotes=upvotes, creator=some_user)
        post.tags.all()
        post.tags.add(request.POST['post_tags'])#Adding tags to the object created.

        """
        active_user = User.objects.get(username=request.user.username)
        print "Active User: "
        print active_user.username

        creator = active_user.id
        post.creator = creator
        """


        """
        active_user = UserProfile.objects.get(user=request.user.id)
        #print active_user.username
        creator = active_user.id
        post.creator = creator
        post.save()
        """

        que_dict = {
            'que': post,
            'user': request.user,
        }

        return render_to_response('post_question.html', que_dict, context)

    else:
        if request.user.is_authenticated():
            user = request.user
            c = {'user': user}
            print user.username
        else:
            err_msg = "You need to login to post a question."
            c = {'err_msg': err_msg}

        c.update(csrf(request))
        return render_to_response('ask_question.html', c)


def view_tags(request):
    context = RequestContext(request)
    tags = Tag.objects.all()
    for i in tags:
        i.count = len(Post.objects.filter(tags=i))
    context_dict = {'tags': tags}
    return render_to_response('forum/tags.html', context_dict, context)

def search_tags(request):
    """
        @AJAX SEARCHING
        @author = d27
    """

    search_dict = {}

    if request.method == 'POST':
        search_text = request.POST['search_text']
        searched_tags = Tag.objects.filter(name__contains=search_text)
        search_dict = {
            'searched_tags': searched_tags
        }
    else:
        search_text = "No query provided."
        print search_text

    render_to_response('search.html', search_dict)
