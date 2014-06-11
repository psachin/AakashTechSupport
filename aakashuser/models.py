# Create your models here.
__author__ = 'ushubham27'

from django.db import models
from django.db.models import *
from django.contrib.auth.models import User
from django.contrib import admin
from django.db.models.signals import post_save
from taggit.managers import TaggableManager
#from shared.utils import *


class UserProfile(models.Model):
    avatar = models.ImageField("Profile Pic", upload_to="avatar", blank=True, null=True)
    posts = models.IntegerField(default=0)
    replies = models.IntegerField(default=0)
    user = OneToOneField(User, related_name="profile")

    def __unicode__(self):
        return self.user.username

    def increment_posts(self):
        self.posts += 1
        self.save()

    def increment_replies(self):
        self.replies += 1
        self.save()

class Category(Model):
    title = CharField(max_length=60)
    description = TextField(max_length=500)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse2("forum", dpk=self.pk)


class Post(Model):
    title = CharField(max_length=60)
    created = DateTimeField(auto_now_add=True)
    creator = ForeignKey(User, blank=True, null=True)
    body = TextField()
    category = ForeignKey(Category, related_name="posts")
    tags = TaggableManager()
    vote = IntegerField(default=0)


    class Meta:
        ordering = ["created"]

    def __unicode__(self):
        return u"%s" % (self.title)

    def increment_vote(self):
        self.vote += 1
        self.save()

    def short(self):
        created = self.created.strftime("%b %d, %I:%M %p")
        return u"%s - %s\n%s" % (self.creator, self.title, created)

    def profile_data(self):
        p = self.created.profile
        return p.posts, p.avatar


class Reply(Model):
    title = ForeignKey(Post, related_name="post")
    created = DateTimeField(auto_now_add=True)
    creator = ForeignKey(User, blank=True, null=True)
    body = TextField()
    vote = IntegerField(default=0)


    class Meta:
        ordering = ["created"]

    def __unicode__(self):
        return u"%s" % (self.title)

    def increment_vote(self):
        self.vote += 1
        self.save()

    def short(self):
        created = self.created.strftime("%b %d, %I:%M %p")
        return u"%s - %s\n%s" % (self.creator, self.title, created)

    def profile_data(self):
        p = self.created.profile
        return p.posts, p.avatar


class Comment(Model):
    comment = ForeignKey(Reply)
    body = TextField()
    created = DateTimeField(auto_now_add=True)
    creator = ForeignKey(User, blank=True, null=True)
    vote = IntegerField(default=0)

    class Meta:
        ordering = ["-created"]

    def __unicode__(self):
        return unicode("%s - %s(title)" % (self.title, self.forum))
