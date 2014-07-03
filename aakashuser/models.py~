from django.db import models
#from django.contrib.auth.models import User
from django.contrib import admin
from django.db.models.signals import post_save

# Create your models here.

class User (models.Model):
	tab_id = models.IntegerField()
	email_id = models.EmailField(max_length = 75)
	location = models.CharField(max_length = 100)
	password = models.CharField(max_length = 100)
	
	def __unicode__(self):
		return self.email_id

"""	

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

"""
