from aakashuser.models import *
from django import forms
from django.contrib.auth.models import User
import datetime
from datetime import timedelta


class SubmitTicketForm(forms.ModelForm):
    tab_id = forms.CharField(max_length=8, help_text="Enter your tablet  id:")
    topic_id = forms.ChoiceField(choices=[(x['category'], str(x['category'])) for x in Category.objects.values(
        'category')], help_text="Select the category of your problem:")#topic_id will display a html select element in the rendered html so that the user can select his problems category
    message = forms.CharField(max_length=500, help_text="message :",
                              widget=forms.widgets.Textarea(attrs={'cols': 35, 'rows': 5}))#a textarea is displayed in the rendered html
    created_date_time = forms.DateTimeField(
        widget=forms.TextInput(attrs={'readonly': 'readonly', 'hidden': 'True'}), initial=datetime.datetime.now)#is a hidden and readonly field in the rendered html with the initial value as the current datetime
    overdue_date_time = forms.DateTimeField(
        widget=forms.TextInput(attrs={'readonly': 'readonly', 'hidden': 'True'}), initial=datetime.datetime.now)#is a hidden and readonly field in the rendered html with the initial value as the current datetime
    closed_date_time = forms.DateTimeField(
        widget=forms.TextInput(attrs={'readonly': 'readonly', 'hidden': 'True'}), initial=datetime.datetime.now)#is a hidden and readonly field in the rendered html with the initial value as the current datetime
    status = forms.IntegerField(
        widget=forms.TextInput(attrs={'readonly': 'readonly', 'hidden': 'True'}), initial=0)#is a hidden and readonly field in the rendered html with the initial value as 0 i.e open
    reopened_date_time = forms.DateTimeField(
        widget=forms.TextInput(attrs={'readonly': 'readonly', 'hidden': 'True'}), initial=datetime.datetime.now)
#is a hidden and readonly field in the rendered html with the initial value as the current datetime
    topic_priority = forms.IntegerField(
        widget=forms.TextInput(attrs={'readonly': 'readonly', 'hidden': 'True'}), initial=1)
#is a hidden and readonly field in the rendered html with the initial value as 2 i.e. normal priority
    duration_for_reply = forms.IntegerField(
        widget=forms.TextInput(attrs={'readonly': 'readonly', 'hidden': 'True'}), initial=24)#is a hidden and readonly field in the rendered html with the initial value 24 which represents the number of hours

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
                                                  widget=forms.TextInput(attrs={'readonly': 'readonly', 'value': user_details}))#is a readonly field in the rendered html with the initial value as the users email id

    def clean(self):
	#in the clean method we validate the tablet id and raise a ValidationError if the user enters an invalid tablet id
        cleaned_data = self.cleaned_data
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
