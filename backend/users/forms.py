from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User



class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ('name','username', 'gender','email', 'password', 'phoneno', 'confirm_password')