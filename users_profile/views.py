from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm
# Create your views here.


def home(request):
    return render(request, 'users_profile/home.html')
def login(request):
    return render(request, 'users_profile/login.html')

def register(request):
    if request.method=="POST":
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(request,f'Account Created for {username}')
            return redirect('booking-home')
            
    else:
        form=UserRegisterForm()
    return render(request,'users_profile/register.html',{'form':form})

