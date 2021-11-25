from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm
from .models import Ticket
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
import random

from django.contrib.auth.models import User
# Create your views here.


def home(request):
    return render(request, 'users_profile/home.html')


def register(request):
    if request.method=="POST":
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            us=User.objects.filter(username=username).first()
            us.is_active=False
            us.save()
            return redirect('otp',username,email)
            
    else:
        form=UserRegisterForm()
    return render(request,'users_profile/register.html',{'form':form})


def otp(request,username,email):
        otp=random.randrange(100000,999999)
        subject, from_email, to = 'welcome', 'aduser.movie30@gmail.com', email
        html_content = f"Your email registered with {username}.Please Enter this OTP:{otp}"
        msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        context={'otp':otp,'username':username}
        return render(request,'users_profile/otp.html',context)


def validate_otp(request):
    usr_otp=request.POST.get('otp2','')
    otp =request.POST.get('otp','')
    username=request.POST.get('username','')
    us=User.objects.filter(username=username).first()
    if int(otp)==int(usr_otp):
        us.is_active=True
        us.save()
        messages.success(request,f'Account Created for {username}')
        return redirect('booking-home')
    else:
        us.delete()
        messages.success(request,"OTP not matching TRY AGAIN")
        return redirect('register')



@login_required
def profile(request):
    current_user = request.user
    context = {'tickets': Ticket.objects.filter(user=current_user)}
    return render(request,'users_profile/profile.html', context)
