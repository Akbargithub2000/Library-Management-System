from django import forms
from django.contrib.auth.models import User
from . import models

class IssueBookForm(forms.Form):
    isbn2 = forms.ModelChoiceField(queryset=models.Book.objects.all(), empty_label="Book Name", to_field_name="isbn", label="Book")
    name2 = forms.ModelChoiceField(queryset=models.Members.objects.all(), empty_label="Name", to_field_name="user", label="Member Details")
    amount_paid = forms.IntegerField()
    
    isbn2.widget.attrs.update({'class': 'form-control'})
    name2.widget.attrs.update({'class':'form-control'})
    amount_paid.widget.attrs.update({'class':'form-control'})
