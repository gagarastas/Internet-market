from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email=forms.EmailField()
    class Meta():
        model=User
        fields=('username','email','password1','password2')
    def __init__(self,*args, **kwargs):
        super(RegisterForm,self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class':"form-control form-control-lg",'placeholder':'username'})
        self.fields['email'].widget.attrs.update({'class':"form-control form-control-lg",'placeholder':'email'})
        self.fields['password1'].widget.attrs.update({'class':"form-control form-control-lg",'placeholder':'password'})
        self.fields['password2'].widget.attrs.update({'class': "form-control form-control-lg",'placeholder':'repeat password'})
