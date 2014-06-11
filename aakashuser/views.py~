# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.context_processors import csrf
from django.contrib import auth
from aakashuser.models import User
from aakashuser.forms import RegisterForm

# INDEX PAGE VIEW

def index(request):
	return render_to_response("index.html", request)

# REGISTER VIEW

def register(request):
	context = RequestContext(request)
	er1 = ""
	if request.POST:
		postform = RegisterForm(data=request.POST)
	
		if postform.is_valid():
			pwd = request.POST['password']
			rpwd = request.POST['repassword']
	
			if pwd == rpwd:
				postform.save(commit=True)
				return HttpResponseRedirect('/index/')
			else:
				er1 = "Passwords don't match"
		else:
			print postform.errors
	else:
		postform = RegisterForm()
		print postform # Not Neccessary
		
	context_dict = {
		'postform' : postform,
		'er1' : er1,
	}
		
	return render_to_response("register.html", context_dict, context)
		
# LOGIN VIEW

def login(request):
	session_id=""
	if request.method == 'POST':
		try:
		    m = User.objects.get(email_id=request.POST['email_id'])
		    if m.password == request.POST['password']:
		        request.session['id'] = m.email_id
		        session_id = request.session['id']
		        
		    	login_dict = {
					'm' : m,
					'session_id' : session_id,
		    	}
		        return render(request, 'index.html', login_dict)
		except User.DoesNotExist:
		    return HttpResponse("Your email_id and password didn't match.")		            
	else:
		c={}
		c.update(csrf(request))
		context=RequestContext(request)
		return render_to_response("login.html", c, context)
       
def logout(request):
    try:
        del request.session['id']
        msg = "You have been succesfully logged out."
        print msg
    except KeyError:
    	msg = "KeyError : Unable to Logout "
        print msg
    
    logout_msg = {
    	'msg' : msg
    }
    
    return HttpResponseRedirect('/index/', logout_msg)

