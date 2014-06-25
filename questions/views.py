# Create your views here.
import datetime
from django.contrib.auth.models import User

from django.template import RequestContext
from django.shortcuts import render_to_response, render, get_object_or_404
from aakashuser.models import Post, Reply, UserProfile, Category
from taggit.models import Tag
from django.core.context_processors import csrf

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
        posts = Post.objects.all().order_by("-post_views")
        context_dict = {
            'posts': posts,
        }

    elif url == 'votes':
        posts = Post.objects.all().order_by("-upvotes")
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
        context_dict = {
            'posts': posts,
        }
        c_dict = {
            'url': url
        }
        context_dict.update(c_dict)

    return render_to_response('questions/all_questions.html', context_dict, context)


def ask_question(request):
    context = RequestContext(request)
    if request.POST:
        title = request.POST['post_title']
        body = request.POST['post_text']
        category_selected = request.POST['category']
        post_date = datetime.datetime.now()
        upvotes = 0
        u = User.objects.get(username=request.user.username)
        some_user = UserProfile.objects.get(user=u)

        category_selected = category_selected.upper()
        category = Category.objects.get(category=category_selected)

        post = Post.objects.create(title=title, body=body, post_date=post_date, upvotes=upvotes, creator=some_user,
                                   category=category)
        post.tags.all()
        # Adding tags to the object created.
        post.tags.add(request.POST['post_tags'])

        que_dict = {
            'posts': post,
            'user': request.user,
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

        context_dict = {
            'user': request.user,
            'posts': current_post,
            'post_reply': reply,
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
            return HttpResponse("Error: User has already voted this post :P")
    #This loop is for canceling vote
    elif vote_action == 'recall-vote':
        if (vote_type == 'up') and (thisuserupvote == 1):
            cur_post.userUpVotes.remove(request.user)
        elif (vote_type == 'down') and (thisuserdownvote == 1):
            cur_post.userDownVotes.remove(request.user)
        else:
            return HttpResponse("Error - Unknown vote type or no vote to recall")

    else:
        return HttpResponse("Error: Bad Action.")

    num_votes = cur_post.userUpVotes.count() - cur_post.userDownVotes.count()

    return HttpResponse(num_votes)




def link_question(request, qid):
    context = RequestContext(request)
    question = Post.objects.get(pk=qid)
    posts = Post.objects.get(pk=qid)
    replies = Reply.objects.filter(title=posts)

    context_dict = {
        'user': request.user,
        'posts': posts,
        'replies': replies,
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


def linktag(request, qid):
    context = RequestContext(request)

    new_tag = Tag.objects.get(pk=qid)
    posts_date = Post.objects.filter(tags=new_tag).order_by('-post_date')
    posts_views = Post.objects.filter(tags=new_tag).order_by('-post_views')
    #post = Post.objects.get(tags=new_tag)


    context_dict = {
        'mytag': new_tag,
        'posts_views': posts_views,
        'posts_date': posts_date,
        #'post': post,
    }

    return render_to_response('questions/tagged_questions.html', context_dict, context)


def tag_search(request):
    context = RequestContext(request)
    mytag = request.POST.get('search_text')
    mytag = mytag.upper()
    try:
        new_tag = Tag.objects.get(name=mytag)
        posts = Post.objects.filter(tags=new_tag).order_by('-post_date')
        posts1 = Post.objects.filter(tags=new_tag).order_by('-post_views')
        context_dict = {
            'posts': posts,
            'mytag': new_tag,
            'posts1': posts1
        }
    except Tag.DoesNotExist:
        context_dict = {}
    return render_to_response('questions/all_questions.html', context_dict, context)


