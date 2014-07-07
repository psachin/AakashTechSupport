# Create your views here.
import datetime
from django.contrib.auth.models import User

from django.template import RequestContext
from django.shortcuts import render_to_response, render, get_object_or_404
from aakashuser.models import Post, Reply, UserProfile, Category, Ticket
from taggit.models import Tag
from django.core.context_processors import csrf

from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Count
from django.contrib.auth.decorators import login_required, user_passes_test


def all_questions_view(request, url):
    context = RequestContext(request)
    context_dict = {}

    if url == 'latest':
        posts = Post.objects.all().order_by("-post_date")
        posts = Post.objects.filter(post_status=1)

        context_dict = {
            'posts': posts,

        }

    elif url == 'frequent':
        posts = Post.objects.all().order_by("-post_views")
        posts = Post.objects.filter(post_status=1)
        context_dict = {
            'posts': posts,

        }

<<<<<<< HEAD
    elif url == 'votes':

        posts=Post.objects.all().order_by("-upvotes")
    
        posts = Post.objects.all().order_by("-upvotes")
=======
    elif url == 'num_votes':
        posts = Post.objects.all().order_by("-num_votes")
        posts = Post.objects.filter(post_status=1)
>>>>>>> faeb44b15c2fa16f2d9460b642ee14c55b7551a9
        context_dict = {

            'posts': posts,
        }

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
        posts = Post.objects.filter(post_status=1)

        context_dict = {
            'posts': posts,

        }

    c_dict = {
        'url': url
    }
    context_dict.update(c_dict)

    return render_to_response('questions/all_questions.html', context_dict, context)


<<<<<<< HEAD
def view_tags(request): #This view has been defined for displaying all the tags and the number of posts related to each tag.
	context=RequestContext(request)
	tags=Tag.objects.all()#for fetching all the tags.
	for tag in tags:
		tag.count=len(Post.objects.filter(tags=tag,post_status=1))
	context_dict= {'tags': tags}
	return render_to_response('forum/tags.html', context_dict, context)

=======
>>>>>>> faeb44b15c2fa16f2d9460b642ee14c55b7551a9

def ask_question(request):
    context = RequestContext(request)
    if request.POST:
        title = request.POST['post_title']
        body = request.POST['post_text']
        category_selected = request.POST['category']
        post_date = datetime.datetime.now()
        u = User.objects.get(username=request.user.username)
        some_user = UserProfile.objects.get(user=u)

        category_selected = category_selected.upper()
        category = Category.objects.get(category=category_selected)

        post = Post.objects.create(title=title, body=body, post_date=post_date, creator=some_user,
                                   category=category)
        post.tags.all()
        # Adding tags to the object created.
        post.tags.add(request.POST['post_tags'])

        thisuserupvote = post.userUpVotes.filter(id=request.user.id).count()
        thisuserdownvote = post.userDownVotes.filter(id=request.user.id).count()

        print "User Upvote and Downvote: "
        print thisuserupvote

        print thisuserdownvote
        net_count = post.userUpVotes.count() - post.userDownVotes.count()
        que_dict = {
            'posts': post,
            'user': request.user,
            'thisUserUpvote': thisuserupvote,
            'thisUserDownvote': thisuserdownvote,
            'net_count': net_count
        }
        return render_to_response('questions/question_page.html', que_dict, context)

    else:
        if request.user.is_authenticated():
            user = request.user
            categories = Category.objects.all()
            c = {
                'user': user,
                'catg': categories
            }
            print user.username
        else:
            err_msg = "You need to login to post a question."
            c = {'err_msg': err_msg}

        c.update(csrf(request))
        return render_to_response('questions/ask_question.html', c)


def submit_reply(request, qid):
    context = RequestContext(request)
    context_dict = {}

    if request.POST:
        current_post = Post.objects.get(pk=qid)
        print current_post.creator
        print current_post.title

        reply_body = request.POST['post_answer']
        upvotes = 0

        u = User.objects.get(username=request.user.username)
        some_user = UserProfile.objects.get(user=u)

        reply = Reply.objects.create(title=current_post, body=reply_body, upvotes=upvotes, user=some_user)
        print reply.reply_date

        replies = Reply.objects.filter(title=current_post)

        thisuserupvote = current_post.userUpVotes.filter(id=request.user.id).count()
        thisuserdownvote = current_post.userDownVotes.filter(id=request.user.id).count()
        net_count = current_post.userUpVotes.count() - current_post.userDownVotes.count()

        context_dict = {
            'user': request.user,
            'posts': current_post,
            'post_replies': replies,
            'thisUserUpvote': thisuserupvote,
            'thisUserDownvote': thisuserdownvote,
            'net_count': net_count
        }

    else:
        return HttpResponse("Reply failed to process..")

    return render_to_response('questions/question_page.html', context_dict, context)


def vote_post(request):
    post_id = int(request.POST.get('id'))
    vote_type = request.POST.get('type')
    vote_action = request.POST.get('action')

    cur_post = get_object_or_404(Post, pk=post_id)

    thisuserupvote = cur_post.userUpVotes.filter(id=request.user.id).count()
    thisuserdownvote = cur_post.userDownVotes.filter(id=request.user.id).count()

    initial_votes = cur_post.userUpVotes.count() - cur_post.userDownVotes.count()

    # print "User Initial Upvote and Downvote: %d %d %s " % (thisuserupvote, thisuserdownvote, vote_action)

    #This loop is for voting
    if vote_action == 'vote':
        if (thisuserupvote == 0) and (thisuserdownvote == 0):
            if vote_type == 'up':
                cur_post.userUpVotes.add(request.user)
            elif vote_type == 'down':
                cur_post.userDownVotes.add(request.user)
            else:
                return HttpResponse("Error: Unknown vote-type passed.")
        else:
            return HttpResponse(initial_votes)
    #This loop is for canceling vote
    elif vote_action == 'recall-vote':
        if (vote_type == 'up') and (thisuserupvote == 1):
            cur_post.userUpVotes.remove(request.user)
        elif (vote_type == 'down') and (thisuserdownvote == 1):
            cur_post.userDownVotes.remove(request.user)
        else:
            # "Error - Unknown vote type or no vote to recall"
            return HttpResponse(initial_votes)
    else:
        return HttpResponse("Error: Bad Action.")

    num_votes = cur_post.userUpVotes.count() - cur_post.userDownVotes.count()
    cur_post.num_votes = num_votes
    cur_post.save()

    print "Num Votes: %s" % num_votes

    return HttpResponse(num_votes)


def link_question(request, qid):
    context = RequestContext(request)
    posts = Post.objects.get(pk=qid)
    replies = Reply.objects.filter(title=posts)

    thisuserupvote = posts.userUpVotes.filter(id=request.user.id).count()
    thisuserdownvote = posts.userDownVotes.filter(id=request.user.id).count()

    net_count = posts.userUpVotes.count() - posts.userDownVotes.count()

    context_dict = {
        'user': request.user,
        'posts': posts,
        'post_replies': replies,
        'thisUserUpvote': thisuserupvote,
        'thisUserDownvote': thisuserdownvote,
        'net_count': net_count
    }

    return render_to_response('questions/question_page.html', context_dict, context)


def view_tags(request):
    context = RequestContext(request)
    tags = Category.objects.all()

    for i in tags:
        i.count = len(Post.objects.filter(category=i))

    context_dict = {
        'tags': tags
    }
    return render_to_response('questions/tags.html', context_dict, context)


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


def linktag(request, qid):
    context = RequestContext(request)

    new_tag = Tag.objects.get(pk=qid)
    posts_date = Post.objects.filter(tags=new_tag,post_status=1).order_by('-post_date')#for fetching posts related to a particular tag.
    posts_views = Post.objects.filter(tags=new_tag,post_status=1).order_by('-post_views')
    cat = Category.objects.get(pk=qid)
    posts_date = Post.objects.filter(category=cat).order_by('-post_date')
    posts_views = Post.objects.filter(category=cat).order_by('-post_views')
    #post = Post.objects.get(tags=new_tag)

    context_dict = {
        'mytag': cat,
        'posts_views': posts_views,
        'posts_date': posts_date,
        #'post': post,
    }

    return render_to_response('questions/tagged_questions.html', context_dict, context)    
    

def tag_search(request):#This view has been defined to search a tag, and if found , display the associated questions.
	context=RequestContext(request)
	mytag = request.POST.get('search_text')#value of search_text comes through the textbox in html
	mytag=mytag.upper()
	try:
		new_tag= Tag.objects.get(name=mytag)
		posts=Post.objects.filter(tags=new_tag,post_status=1).order_by('-post_date')#for fetching posts related to a particular tag.
		posts1= Post.objects.filter(tags=new_tag,post_status=1).order_by('-post_views')
		context_dict={
			'posts':posts,
			'mytag':new_tag,
			'posts1':posts1}
	except Tag.DoesNotExist:
		context_dict={}
	return render_to_response('questions/all_questions.html', context_dict, context)


def link_question(request, qid):
    context = RequestContext(request)

    posts = Post.objects.get(pk=qid)
    replies = Reply.objects.filter(title=posts).order_by("-upvotes")
    posts.post_views = posts.post_views + 1
    posts.save()
    context_dict = {
        'posts': posts,
        'replies': replies,
    }

    return render_to_response('questions/allqueries_link.html', context_dict, context)


def tag_search(request):
    context = RequestContext(request)
    mytag = request.POST.get('search_text')
    active_user = request.user
    mytag = mytag.upper()

    new_tags = Category.objects.filter(category__icontains=mytag)

    if new_tags.exists():
        context_dict = {
            'tags': new_tags
        }
    else:
        error_msg = "Sorry! No such Category found..."
        context_dict = {
            'error_msg': error_msg
        }

    return render_to_response('questions/tags.html', context_dict, context)


def search(request):
    if request.method == "POST":
        Search = request.POST.get('search')
        active_user = request.user
        count_open = Ticket.objects.filter(status=0).count()
        count_close = Ticket.objects.filter(status=1).count()
        context_dict = {}

        """Searching for ticket-id"""
        tickets = Ticket.objects.filter(Q(ticket_id__icontains=Search) | Q(user_id__icontains=Search))

<<<<<<< HEAD
def link_question(request, qid):
    context = RequestContext(request)
    question = Post.objects.get(pk=qid)
    posts = Post.objects.get(pk=qid)
    replies = Reply.objects.filter(title=posts)
   
    context_dict = {
        'posts': posts,
        'replies': replies,
    }

    return render_to_response('questions/allqueries_link.html', context_dict, context)

=======
        if tickets.exists():
            context_dict = {
                'user': active_user,
                'tickets': tickets,
                'count_open': count_open,
                'count_close': count_close,
            }
            return render_to_response("ticketing/search.html", context_dict, RequestContext(request))
        else:
            """Searching for Topic-id"""
            tickets = Category.objects.filter(category__icontains=Search)

            if tickets.exists():
                tickets = Ticket.objects.filter(topic_id=tickets)
                context_dict = {
                    'user': active_user,
                    'tickets': tickets,
                    'count_open': count_open,
                    'count_close': count_close,
                }
                return render_to_response("ticketing/search.html", context_dict, RequestContext(request))
            else:
                tickets = Ticket.objects.all()
                context_dict = {
                    'user': active_user,
                    'tickets': tickets,
                    'count_open': count_open,
                    'count_close': count_close,
                }
                return render_to_response("ticketing/d.html", context_dict, RequestContext(request))
>>>>>>> faeb44b15c2fa16f2d9460b642ee14c55b7551a9
