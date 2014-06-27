from aakashuser.models import *
from django import forms
from django.contrib.auth.models import User
import datetime
from datetime import timedelta
import re
def special_match(strg, search=re.compile(r'[^a-z0-9.]').search):
    	return not bool(search(strg))

class SubmitTicketForm(forms.ModelForm):
    tab_id = forms.CharField(
			    max_length=8,
			    error_messages={
			    'required': 'Tablet id is required.'
			    },
			    help_text="Enter your tablet  id:",
			    label="Table id",
			    widget=forms.TextInput(
				    attrs={'class': 'form-control', 'placeholder': 'Tablet Id'}),
			    )
    topic_id = forms.ChoiceField(
			    choices=[(x['category'], str(x['category'])) for x in Category.objects.values('category')],
			    help_text="Enter Help Topic:",
			    #label="Select Help Topic",
			    widget=forms.Select(
				    attrs={'class': 'form-control', 'placeholder': 'Help topic'}),
			    )#topic_id will display a html select element in the rendered html so that the user can select his problems category
    message = forms.CharField(max_length=500,
			      help_text="Message :",
			      label="Message",
			      widget=forms.Textarea(attrs={'class': 'form-control'})
                             )#a textarea is displayed in the rendered html
    class Meta:
        model = Ticket
        fields = ('tab_id', 'user_id', 'topic_id', 'message')

    def clean_topic_id(self):
        category = Category.objects.get(category=self.cleaned_data['topic_id'])
        return category

    def __init__(self, *args, **kwargs):
        # client is the parameter passed from views.py
        user_details = kwargs.pop("user_details")#get the users email from the argument passed
        super(SubmitTicketForm, self).__init__(*args, **kwargs)
        self.fields['user_id'] = forms.EmailField(help_text="Enter your email  id:",
						  label="Email id",
                                                  widget=forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly', 'value': user_details}))#is a readonly field in the rendered html with the initial value as the users email id
    
    	
    def clean(self):
	#in the clean method we validate the tablet id and raise a ValidationError if the user enters an invalid tablet id
        cleaned_data = self.cleaned_data
	if special_match(cleaned_data.get('tab_id')) and cleaned_data.get('message')!="":
		entered_tab_id = int(cleaned_data.get('tab_id'))#get the entered tab id
		tablets = Tablet_info.objects.all()#get all the tablets from the Tablet_info table
		found = 0
		for tablet in tablets:
		    starttab = tablet.start_tab_id
		    endtab = tablet.end_tab_id
		    if starttab <= entered_tab_id <= endtab:
			#if the tablet id entered is between the starting and ending tablet id ; then the found flag is set as 1 otherwise it stays 0
		        found = 1
		if found == 0:
		    #raise a ValidationError if the tab id is invalid	
		    raise forms.ValidationError(
		        "You have entered an invalid tablet id")
		else:
		    return cleaned_data
	else:
		raise forms.ValidationError(
		        "You have entered an invalid tablet id")
