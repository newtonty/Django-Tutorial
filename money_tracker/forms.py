from django.forms import ModelForm
from money_tracker.models import TransactionRecord
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class TransactionRecordForm(ModelForm):
    class Meta:
        model = TransactionRecord
        fields = ["name", "type", "amount", "description"]

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in self.fields:
                self.fields[field].widget.attrs.update({'class': 'form-control'})

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label="Username", 
                                widget=forms.TextInput(attrs={'placeholder': '150 characters or fewer', 'size': '23', 'class': 'form-control'}),
                                error_messages={'required': 'Please enter your username'})
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'At least 8 characters', 'size': '23', 'class': 'form-control'}))
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password again', 'size': '23', 'class': 'form-control'}))
