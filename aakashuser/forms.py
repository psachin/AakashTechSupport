# FORMS
__author__ = 'ushubham27'

from django import forms
from django.contrib.auth.models import User
from tinymce.widgets import TinyMCE

class UserForm(forms.ModelForm):
    username = forms.CharField(label='Username',
        widget= forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Username to login*.'}),
            help_text="",
            required=True,
            error_messages={'required':'Username is required.'})
    first_name = forms.CharField(
        widget= forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Coordinator first name*.'}),
            help_text="",
            required=True,
            error_messages={'required':'First name is required.'})
    last_name = forms.CharField(
        widget= forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Coordinator last name*.'}),
            help_text="",
            required=True,
            error_messages={'required':'Last name is required.'})
    email = forms.CharField(
        widget= forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Coordinator valid email*.'}),
            help_text="",
            required=True,
            error_messages={'required':'Valid Email address is required.'})
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Coordinator password*.'}),
            help_text="",
            required=True,
            error_messages={'required':'Password is missing.'})
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Re-enter password'}),
            help_text="",
            required=True,
            error_messages={'required':'reenter correct password.'})

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'password1']