# FORMS
import datetime
from django.core.validators import RegexValidator

__author__ = 'ushubham27'

from django import forms
from django.contrib.auth.models import User
from tinymce.widgets import TinyMCE
from aakashuser.models import Post, Category, UserProfile


class UserForm(forms.ModelForm):
    username = forms.CharField(
        min_length=6,
        max_length=30,
        required=True,
        error_messages={
            'required': 'Username is required.'
        },
        validators=[
            RegexValidator('^[a-zA-Z0-9]*$', message='Username must be Alphanumeric'),
        ],
        label='Username',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Username to login*.'}),
        )

    first_name = forms.CharField(
        min_length=2,
        max_length=20,
        required=True,
        error_messages={
            'required': 'First name is required.'
        },
        validators=[
            RegexValidator('^[a-zA-Z]*$', message='First name must be Alphanumeric'),
        ],
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Coordinator first name*.'}),
        )

    last_name = forms.CharField(
        min_length=2,
        max_length=20,
        required=True,
        error_messages={
            'required': 'Last name is required.'
        },
        validators=[
            RegexValidator('^[a-zA-Z]*$', message='Last name must be Alphanumeric'),
        ],
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Coordinator last name*.'}),
        )

    email = forms.CharField(
        max_length=30,
        required=True,
        error_messages={
            'required': 'Valid Email address is required.'
        },
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Coordinator valid email*.'}),
        )

    password = forms.CharField(
        min_length=6,
        max_length=16,
        required=True,
        error_messages={
            'required': 'Password is missing.'
        },
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Coordinator password*.'}),

        )

    password1 = forms.CharField(
        min_length=6,
        max_length=16,
        required=True,
        error_messages={
            'required': 'reenter correct password.'
        },
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Re-enter password'}),
        )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'password1']

"""
class PostForm(forms.ModelForm):

    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        ),
        help_text="",
        required=True,
        error_messages={'required:' 'Renter the question tile.'}
    )
    body = forms.Textarea(
        widget=forms.Textarea(
            attrs={
                'class': "form-control",
            }
        ),
        help_text="",
        required=True,
        error_messages={
            'required': 'Re-enter the text.'
        }
    )

    tags = forms.ChoiceField(
        choices=[(x['category'], str(x['category']))
                 for x in Category.objects.values('category')],
        help_text="please select the category of your problem"
    )

    class Meta:
        model = Post
        fields = ['title', 'body', 'tags']

    def clean_created_date_time(self):
        return datetime.datetime.now()

"""

class UserProfileForm(forms.ModelForm):
    location = forms.CharField(
			    max_length=30,
			    error_messages={
			    'required': 'location is required.'
			    },
			    #help_text="Enter your location:",
			    label="Location",
			    required=False,
			    widget=forms.TextInput(
				    attrs={'class': 'form-control', 'placeholder': 'Location'}),
			    )
    skills = forms.CharField(
			    max_length=100,
			    required=False,
			    error_messages={
			    'required': 'skills is required.'
			    },
			    #help_text="Enter your skills:",
			    widget=forms.TextInput(
				    attrs={'class': 'form-control', 'placeholder': 'skills'}),
			    )
    avatar = forms.ImageField(
			    label='Profile picture',
			    required=False,
			     widget=forms.FileInput(attrs={
			     'placeholder': 'Profile picture.'}),
			      )
    class Meta:
        model = UserProfile
        fields = ('location', 'skills','avatar')