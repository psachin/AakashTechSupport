# FORMS
from django import forms
from aakashuser.models import User

class RegisterForm(forms.ModelForm):
	
	tab_id = forms.IntegerField(required=True)
	email_id = forms.EmailField(required=True)
	location = forms.CharField(required=True)
	password = forms.CharField(required=True)
	repassword = forms.CharField(required=True)
	
	class Meta:
		model = User
		fields = ['tab_id', 'email_id', 'location', 'password', 'repassword']
		



