from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email=forms.EmailField()
    Age=forms.IntegerField(min_value=12,max_value=80)
    
    class Meta:
        model = User
        
        fields=['username','email','Age','password1','password2']
        #fields = UserCreationForm.Meta.fields + ("Age",)