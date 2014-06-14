from django.db import models
from django.db.models import *
from django.contrib.auth.models import User
from django.contrib import admin
from django.db.models.signals import post_save
from taggit.managers import TaggableManager

class UserProfile(models.Model):#Model for storing a user's information.
    user = OneToOneField(User)
    location = models.CharField(max_length=10)
    avatar = models.ImageField(upload_to='static/images/profile_image', blank=True)#for storing user's pic
    online_status = models.BooleanField(default=False)
    user_type = models.IntegerField(max_length=1, default=0)
    user_skills = models.CharField(max_length=100, blank=True)#to mantain user profile
    num_of_posts = IntegerField(default=0)
    reply_count = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.username

    def increment_posts(self):
        self.num_of_posts += 1
        self.save()

    def increment_replies(self):
        self.reply_count += 1
        self.save()


class Category(models.Model):#Model for storing categories of various posts.
    category_title = models.CharField(max_length=20)
    description = models.TextField()

    def __unicode__(self):
        return self.category_title

class Post(models.Model):#Model for storing information about each post with category as its foreign key.
    title = CharField(max_length=60)
    body = models.TextField()
    post_date = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(UserProfile)
    #category = models.ForeignKey('Category')
    post_views = models.IntegerField(default=0)#Frequently visited posts
    upvotes = models.IntegerField(default=0)
    tags = TaggableManager()#for storing multiple tags for each question
    post_status = models.IntegerField(max_length=1, default=0)#question will need admin's approval 0 being not approved, 1 being approved and can be displayed

    class Meta:
        ordering = ["post_date"]

    def __unicode__(self):
        return self.title

    def increment_count(self):
        self.count += 1
        self.save()

    def short(self):
        created = self.created_date.strftime("%b %d, %I:%M %p")
        return u"%s - %s\n%s" % (self.user, self.title, self.post_date)


class Reply(models.Model):#Model for storing information about each reply with post as its foreign key.
    title = models.ForeignKey(Post)
    body = models.TextField()#body of the reply
    user = models.ForeignKey(User)
    reply_date = models.DateTimeField(auto_now_add=True)
    file_upload = models.FileField(upload_to='forum/file',blank=True)
    upvotes = models.IntegerField(default=0)
    reply_status = models.BooleanField(default=False)

    class Meta:
        ordering = ["reply_date"]

    def __unicode__(self):
        return unicode(self.pk)

    def short(self):
        created = self.post_date.strftime("%b %d, %I:%M %p")
        return u"%s - %s\n%s" % (self.user, self.title, self.reply_date)

    def profile_data(self):
        p = self.reply_date.profile
        return p.posts, p.avatar


class Comment(models.Model):#Model for storing information about each Comment with Reply as its foreign key.
    ans_id = models.ForeignKey(Reply)
    comment_body = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    comment_status = IntegerField(default=0, max_length=0)

    class Meta:
        ordering = ["-created_date"]

    def __unicode__(self):
        return self.user.username


